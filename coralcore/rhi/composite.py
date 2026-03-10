# 🪸 CORAL-CORE Reef Health Index (Pure Python)
# Version: 1.0.0 | بدون أي اعتماديات خارجية

"""
Reef Health Index Module - Pure Python implementation
لا يحتاج إلى numpy أو أي مكتبات خارجية
"""

from typing import Dict, Optional, Union, List
from dataclasses import dataclass
from datetime import datetime

# =============================================================================
# CONSTANTS
# =============================================================================

# PCA-derived weights
RHI_WEIGHTS = {
    'g_ca': 0.19,
    'e_diss': 0.14,
    'phi_ps': 0.21,
    'rho_skel': 0.12,
    'delta_ph': 0.11,
    's_reef': 0.10,
    'k_s': 0.08,
    't_thr': 0.05
}

# Normalization reference values
NORMALIZATION_REF = {
    'g_ca': {'min': 0.0, 'max': 2.5},
    'e_diss': {'min': 0.0, 'max': 100.0},
    'phi_ps': {'min': 0.0, 'max': 0.80},
    'rho_skel': {'min': 0.5, 'max': 2.0},
    'delta_ph': {'min': 0.0, 'max': 0.25},
    's_reef': {'min': 2.0, 'max': 5.0},
    'k_s': {'min': 0.0, 'max': 0.35},
    't_thr': {'min': 28.0, 'max': 34.0}
}

# Classification thresholds
RHI_STATUS = {
    'healthy': {'threshold': 0.8, 'color': '🟢', 'status': 'HEALTHY'},
    'stressed': {'threshold': 0.5, 'color': '🟡', 'status': 'STRESSED'},
    'critical': {'threshold': 0.0, 'color': '🔴', 'status': 'CRITICAL'}
}


@dataclass
class RHIResult:
    """Container for RHI calculation results"""
    rhi: float
    normalized_params: Dict[str, float]
    contributions: Dict[str, float]
    status: str
    color: str
    timestamp: datetime
    station_id: Optional[str] = None
    uncertainty: Optional[float] = None


class ReefHealthIndex:
    """Reef Health Index calculator - Pure Python implementation."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize RHI calculator.
        """
        self.weights = weights if weights is not None else RHI_WEIGHTS.copy()
        self.history = []
        
        # التحقق من مجموع الأوزان
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            # إعادة تطبيع الأوزان
            for key in self.weights:
                self.weights[key] = self.weights[key] / total
    
    def normalize_parameter(self, param_name: str, value: float) -> float:
        """
        Normalize a parameter to 0-1 scale.
        """
        ref = NORMALIZATION_REF.get(param_name, {'min': 0, 'max': 1})
        
        min_val = ref['min']
        max_val = ref['max']
        
        if max_val <= min_val:
            return 0.5
        
        # Min-max normalization
        norm_value = (value - min_val) / (max_val - min_val)
        
        # Clip to [0, 1]
        if norm_value < 0:
            norm_value = 0
        if norm_value > 1:
            norm_value = 1
        
        return norm_value
    
    def compute(
        self,
        parameters: Dict[str, float],
        station_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        return_full: bool = True
    ) -> Union[float, RHIResult]:
        """
        Compute Reef Health Index from parameters.
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # التحقق من وجود جميع المعاملات
        for param in self.weights.keys():
            if param not in parameters:
                raise ValueError(f"Missing parameter: {param}")
        
        # تطبيع المعاملات
        normalized = {}
        contributions = {}
        total_rhi = 0.0
        
        for param, weight in self.weights.items():
            norm_value = self.normalize_parameter(param, parameters[param])
            normalized[param] = norm_value
            contribution = weight * norm_value
            contributions[param] = contribution
            total_rhi += contribution
        
        # تحديد الحالة
        if total_rhi >= 0.8:
            status_info = {'status': 'HEALTHY', 'color': '🟢'}
        elif total_rhi >= 0.5:
            status_info = {'status': 'STRESSED', 'color': '🟡'}
        else:
            status_info = {'status': 'CRITICAL', 'color': '🔴'}
        
        # حفظ في التاريخ
        self.history.append({
            'timestamp': timestamp,
            'rhi': total_rhi,
            'station_id': station_id
        })
        
        # تحديد حجم التاريخ
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        if not return_full:
            return total_rhi
        
        return RHIResult(
            rhi=total_rhi,
            normalized_params=normalized,
            contributions=contributions,
            status=status_info['status'],
            color=status_info['color'],
            timestamp=timestamp,
            station_id=station_id,
            uncertainty=total_rhi * 0.10
        )
    
    def get_trend(self, days: int = 30) -> Dict:
        """
        Get RHI trend (simple trend without numpy).
        """
        if len(self.history) < 2:
            return {'direction': 'stable', 'rate': 0}
        
        recent = self.history[-min(days, len(self.history)):]
        values = [h['rhi'] for h in recent]
        
        # حساب الاتجاه البسيط
        if len(values) >= 2:
            first = values[0]
            last = values[-1]
            
            if last > first * 1.01:
                direction = 'improving'
                rate = (last - first) / len(values)
            elif last < first * 0.99:
                direction = 'declining'
                rate = (first - last) / len(values)
            else:
                direction = 'stable'
                rate = 0
        else:
            direction = 'stable'
            rate = 0
        
        return {
            'direction': direction,
            'rate': rate
        }
