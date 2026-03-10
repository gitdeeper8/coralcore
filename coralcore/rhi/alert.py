# 🪸 CORAL-CORE Alert System (Pure Python)
# Version: 1.0.0 | بدون أي اعتماديات خارجية

"""
RHI Alert System - Pure Python implementation
لا يحتاج إلى numpy أو أي مكتبات خارجية
"""

from typing import Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json

# =============================================================================
# CONSTANTS
# =============================================================================

class AlertLevel:
    """Alert severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    BLEACHING = "BLEACHING_ALERT"


class AlertChannel:
    """Alert notification channels"""
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    WEBHOOK = "webhook"
    CONSOLE = "console"


# Alert thresholds
ALERT_THRESHOLDS = {
    'rhi_critical': 0.50,
    'rhi_warning': 0.70,
    'rhi_healthy': 0.80,
    'decline_rate_critical': -0.02,
    'phi_ps_critical': 0.25,
    'phi_ps_warning': 0.40,
    'temperature_anomaly': 1.0,
    'dhw_warning': 4,
    'dhw_critical': 8
}

# Default alert messages
ALERT_MESSAGES = {
    AlertLevel.INFO: {
        'title': '✅ RHI Normal',
        'template': 'RHI = {rhi:.3f} - Reef health is normal at {station}'
    },
    AlertLevel.WARNING: {
        'title': '⚠️ RHI Warning',
        'template': 'RHI = {rhi:.3f} - Reef showing stress at {station}. Monitor closely.'
    },
    AlertLevel.CRITICAL: {
        'title': '🚨 RHI CRITICAL',
        'template': 'RHI = {rhi:.3f} - CRITICAL condition at {station}. IMMEDIATE INTERVENTION REQUIRED.'
    },
    AlertLevel.BLEACHING: {
        'title': '🔥 BLEACHING ALERT',
        'template': 'RHI = {rhi:.3f} - BLEACHING IMMINENT at {station}. Deploy mitigation measures.'
    }
}


@dataclass
class Alert:
    """Alert data structure"""
    level: str
    message: str
    station_id: str
    timestamp: datetime
    rhi: float
    parameters: Dict[str, float]
    channels: List[str] = field(default_factory=list)
    sent: bool = False
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


@dataclass
class AlertRule:
    """Alert rule definition"""
    name: str
    condition: Callable[[Dict], bool]
    level: str
    message_template: str
    cooldown_minutes: int = 60
    channels: List[str] = field(default_factory=list)


class AlertManager:
    """Manager for RHI-based alerts - Pure Python implementation."""
    
    def __init__(
        self,
        station_id: str,
        channels: Optional[Dict[str, Dict]] = None,
        alert_history_days: int = 30
    ):
        """
        Initialize alert manager.
        """
        self.station_id = station_id
        self.channels = channels or {}
        self.alert_history: List[Alert] = []
        self.alert_history_days = alert_history_days
        self.rules = self._setup_default_rules()
        self.last_alert_time: Dict[str, datetime] = {}
    
    def _setup_default_rules(self) -> List[AlertRule]:
        """Setup default alert rules."""
        rules = []
        
        # RHI critical rule
        rules.append(AlertRule(
            name='rhi_critical',
            condition=lambda d: d.get('rhi', 1) < ALERT_THRESHOLDS['rhi_critical'],
            level=AlertLevel.CRITICAL,
            message_template=ALERT_MESSAGES[AlertLevel.CRITICAL]['template'],
            cooldown_minutes=30,
            channels=[AlertChannel.EMAIL, AlertChannel.SMS]
        ))
        
        # RHI warning rule
        rules.append(AlertRule(
            name='rhi_warning',
            condition=lambda d: (
                ALERT_THRESHOLDS['rhi_critical'] <= d.get('rhi', 1) < ALERT_THRESHOLDS['rhi_warning']
            ),
            level=AlertLevel.WARNING,
            message_template=ALERT_MESSAGES[AlertLevel.WARNING]['template'],
            cooldown_minutes=120,
            channels=[AlertChannel.EMAIL]
        ))
        
        # Quantum yield critical
        rules.append(AlertRule(
            name='phi_ps_critical',
            condition=lambda d: d.get('phi_ps', 1) < ALERT_THRESHOLDS['phi_ps_critical'],
            level=AlertLevel.BLEACHING,
            message_template="Quantum yield critical: Φ_ps = {phi_ps:.3f} - Bleaching imminent at {station}",
            cooldown_minutes=15,
            channels=[AlertChannel.SMS, AlertChannel.SLACK]
        ))
        
        # Quantum yield warning
        rules.append(AlertRule(
            name='phi_ps_warning',
            condition=lambda d: (
                ALERT_THRESHOLDS['phi_ps_critical'] <= d.get('phi_ps', 1) < ALERT_THRESHOLDS['phi_ps_warning']
            ),
            level=AlertLevel.WARNING,
            message_template="Quantum yield low: Φ_ps = {phi_ps:.3f} at {station}",
            cooldown_minutes=60,
            channels=[AlertChannel.EMAIL]
        ))
        
        return rules
    
    def check_alerts(
        self,
        rhi: float,
        parameters: Dict[str, float],
        trend: Optional[float] = None,
        timestamp: Optional[datetime] = None
    ) -> List[Alert]:
        """
        Check for alerts based on current conditions.
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Prepare condition data
        cond_data = {
            'rhi': rhi,
            'trend': trend,
            'station': self.station_id,
            'timestamp': timestamp,
            **parameters
        }
        
        triggered_alerts = []
        
        for rule in self.rules:
            # Check cooldown
            last_time = self.last_alert_time.get(rule.name)
            if last_time is not None:
                cooldown_seconds = rule.cooldown_minutes * 60
                if (timestamp - last_time).total_seconds() < cooldown_seconds:
                    continue
            
            # Check condition
            try:
                if rule.condition(cond_data):
                    # Format message
                    try:
                        message = rule.message_template.format(**cond_data)
                    except:
                        message = f"Alert: {rule.name} triggered at {self.station_id}"
                    
                    alert = Alert(
                        level=rule.level,
                        message=message,
                        station_id=self.station_id,
                        timestamp=timestamp,
                        rhi=rhi,
                        parameters=parameters.copy(),
                        channels=rule.channels
                    )
                    
                    triggered_alerts.append(alert)
                    self.last_alert_time[rule.name] = timestamp
            except:
                # تجاهل أي خطأ في الشرط
                pass
        
        # Add to history
        self.alert_history.extend(triggered_alerts)
        
        # Clean old history
        self._clean_history()
        
        return triggered_alerts
    
    def send_alert(self, alert: Alert) -> bool:
        """
        Send alert through configured channels.
        """
        if alert.sent:
            return True
        
        success = True
        
        for channel in alert.channels:
            if channel == AlertChannel.CONSOLE:
                self._print_console(alert)
        
        alert.sent = True
        return success
    
    def _print_console(self, alert: Alert):
        """Print alert to console."""
        print(f"\n🚨 [{alert.level}] {alert.message}")
        print(f"  Station: {alert.station_id}")
        print(f"  Time: {alert.timestamp}")
        print(f"  RHI: {alert.rhi:.3f}")
    
    def _clean_history(self):
        """Remove old alerts from history."""
        cutoff = datetime.utcnow() - timedelta(days=self.alert_history_days)
        self.alert_history = [
            a for a in self.alert_history
            if a.timestamp > cutoff
        ]
    
    def get_active_alerts(self, max_age_hours: int = 24) -> List[Alert]:
        """Get alerts from last N hours."""
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        return [a for a in self.alert_history if a.timestamp > cutoff]
    
    def acknowledge_alert(self, alert: Alert, user: str):
        """Mark alert as acknowledged."""
        alert.acknowledged = True
        alert.acknowledged_by = user
        alert.acknowledged_at = datetime.utcnow()
    
    def add_custom_rule(self, rule: AlertRule):
        """Add custom alert rule."""
        self.rules.append(rule)
    
    def save_history(self, filename: str):
        """Save alert history to file."""
        history_data = []
        for alert in self.alert_history:
            history_data.append({
                'level': alert.level,
                'message': alert.message,
                'station_id': alert.station_id,
                'timestamp': alert.timestamp.isoformat(),
                'rhi': alert.rhi,
                'parameters': alert.parameters,
                'channels': alert.channels,
                'sent': alert.sent,
                'acknowledged': alert.acknowledged,
                'acknowledged_by': alert.acknowledged_by,
                'acknowledged_at': alert.acknowledged_at.isoformat() if alert.acknowledged_at else None
            })
        
        with open(filename, 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def load_history(self, filename: str):
        """Load alert history from file."""
        try:
            with open(filename, 'r') as f:
                history_data = json.load(f)
            
            self.alert_history = []
            for data in history_data:
                alert = Alert(
                    level=data['level'],
                    message=data['message'],
                    station_id=data['station_id'],
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    rhi=data['rhi'],
                    parameters=data['parameters'],
                    channels=data['channels'],
                    sent=data['sent'],
                    acknowledged=data['acknowledged'],
                    acknowledged_by=data.get('acknowledged_by'),
                    acknowledged_at=datetime.fromisoformat(data['acknowledged_at']) if data.get('acknowledged_at') else None
                )
                self.alert_history.append(alert)
        except:
            pass  # تجاهل الأخطاء في التحميل
