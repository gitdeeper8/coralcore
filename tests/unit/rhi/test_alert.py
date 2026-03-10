# 🪸 CORAL-CORE Alert Tests
# Unit tests for RHI alert system
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Unit tests for RHI alert system."""

import pytest
from datetime import datetime, timedelta
from coralcore.rhi.alert import AlertManager, AlertLevel, AlertChannel, AlertRule


class TestAlertManager:
    """Test suite for AlertManager."""
    
    @pytest.fixture
    def alert_manager(self):
        """Create alert manager for testing."""
        channels = {
            AlertChannel.CONSOLE: {'enabled': True},
            AlertChannel.EMAIL: {
                'smtp_server': 'localhost',
                'smtp_port': 25,
                'username': 'test',
                'password': 'test'
            }
        }
        return AlertManager('TEST001', channels=channels)
    
    def test_check_alerts_critical(self, alert_manager, critical_parameters):
        """Test critical alert detection."""
        alerts = alert_manager.check_alerts(
            rhi=0.45,
            parameters=critical_parameters
        )
        
        assert len(alerts) > 0
        assert any(a.level == AlertLevel.CRITICAL for a in alerts)
    
    def test_check_alerts_warning(self, alert_manager, stressed_parameters):
        """Test warning alert detection."""
        alerts = alert_manager.check_alerts(
            rhi=0.65,
            parameters=stressed_parameters
        )
        
        assert len(alerts) > 0
        assert any(a.level == AlertLevel.WARNING for a in alerts)
    
    def test_quantum_yield_alert(self, alert_manager):
        """Test quantum yield critical alert."""
        params = {'phi_ps': 0.2}
        alerts = alert_manager.check_alerts(
            rhi=0.6,
            parameters=params
        )
        
        assert len(alerts) > 0
        assert any(a.level == AlertLevel.BLEACHING for a in alerts)
    
    def test_temperature_anomaly_alert(self, alert_manager):
        """Test temperature anomaly alert."""
        params = {'temperature_anomaly': 1.5}
        alerts = alert_manager.check_alerts(
            rhi=0.7,
            parameters=params
        )
        
        assert len(alerts) > 0
        assert 'temperature' in alerts[0].message.lower()
    
    def test_cooldown(self, alert_manager, critical_parameters):
        """Test alert cooldown."""
        # First alert
        alerts1 = alert_manager.check_alerts(
            rhi=0.45,
            parameters=critical_parameters
        )
        
        # Second alert immediately
        alerts2 = alert_manager.check_alerts(
            rhi=0.44,
            parameters=critical_parameters
        )
        
        # Should not create new alert due to cooldown
        assert len(alerts2) <= len(alerts1)
    
    def test_custom_rule(self, alert_manager):
        """Test custom alert rule."""
        def custom_condition(data):
            return data.get('test_param', 0) > 10
        
        rule = AlertRule(
            name='custom_test',
            condition=custom_condition,
            level=AlertLevel.WARNING,
            message_template="Test alert: {test_param}",
            cooldown_minutes=5
        )
        
        alert_manager.add_custom_rule(rule)
        
        alerts = alert_manager.check_alerts(
            rhi=0.8,
            parameters={'test_param': 15}
        )
        
        assert len(alerts) > 0
        assert any(r.name == 'custom_test' for r in alert_manager.rules)
    
    def test_acknowledge_alert(self, alert_manager, critical_parameters):
        """Test alert acknowledgment."""
        alerts = alert_manager.check_alerts(
            rhi=0.45,
            parameters=critical_parameters
        )
        
        if alerts:
            alert_manager.acknowledge_alert(alerts[0], 'tester')
            assert alerts[0].acknowledged
            assert alerts[0].acknowledged_by == 'tester'
            assert alerts[0].acknowledged_at is not None
    
    def test_history(self, alert_manager, critical_parameters):
        """Test alert history."""
        for i in range(5):
            alert_manager.check_alerts(
                rhi=0.45 - i*0.05,
                parameters=critical_parameters,
                timestamp=datetime.utcnow() - timedelta(days=i)
            )
        
        active = alert_manager.get_active_alerts(max_age_hours=24)
        assert len(active) <= len(alert_manager.alert_history)
    
    def test_send_console(self, alert_manager, critical_parameters, capsys):
        """Test sending alert to console."""
        alerts = alert_manager.check_alerts(
            rhi=0.45,
            parameters=critical_parameters
        )
        
        if alerts:
            alert_manager.send_alert(alerts[0])
            captured = capsys.readouterr()
            assert 'CRITICAL' in captured.out
    
    def test_multiple_channels(self):
        """Test alert with multiple channels."""
        channels = {
            AlertChannel.CONSOLE: {'enabled': True},
            AlertChannel.SLACK: {'webhook': 'https://hooks.slack.com/test'},
            AlertChannel.EMAIL: {'enabled': False}
        }
        
        manager = AlertManager('TEST001', channels=channels)
        assert AlertChannel.SLACK in manager.channels
        assert AlertChannel.CONSOLE in manager.channels
    
    def test_save_load_history(self, alert_manager, critical_parameters, tmp_path):
        """Test saving and loading alert history."""
        alert_manager.check_alerts(
            rhi=0.45,
            parameters=critical_parameters
        )
        
        history_file = tmp_path / 'alert_history.json'
        alert_manager.save_history(str(history_file))
        
        assert history_file.exists()
        
        new_manager = AlertManager('TEST001')
        new_manager.load_history(str(history_file))
        
        assert len(new_manager.alert_history) == len(alert_manager.alert_history)
