# 🪸 CORAL-CORE Quantum Yield Module (Pure Python)
# Version: 1.0.0 - نسخة مبسطة للغاية

"""
Zooxanthellae Quantum Yield Module - Pure Python implementation
"""

# =============================================================================
# CONSTANTS
# =============================================================================

QUANTUM_YIELD_THRESHOLDS = {
    'optimal_min': 0.60,
    'optimal_max': 0.72,
    'photoinhibition_max': 0.40,
    'bleaching_max': 0.25,
    'theoretical_max': 0.80
}

PHOTOSYNTHESIS_THRESHOLDS = {
    'optimal': 0.65,
    'stressed': 0.40,
    'bleaching': 0.25
}


def quantum_yield(
    f_m: float = 1200.0,
    f_0: float = 400.0,
    temperature: float = 28.0,
    light_level: float = 1000.0,
    skeletal_amplification: bool = True,
    return_full: bool = False
) -> float:
    """
    Calculate Photosystem II quantum yield.
    
    Parameters
    ----------
    f_m : float
        Maximum fluorescence
    f_0 : float
        Minimum fluorescence
    temperature : float
        Water temperature (°C)
    light_level : float
        Light intensity (μmol photons m⁻² s⁻¹)
    skeletal_amplification : bool
        Account for skeletal light amplification
    return_full : bool
        Return full result
    
    Returns
    -------
    float
        Quantum yield Φ_ps
    """
    if f_m <= 0:
        return 0.0
    
    # حساب العائد الكمي الأساسي
    f_v = f_m - f_0
    phi_ps = f_v / f_m
    
    # ضبط حسب درجة الحرارة (تبسيط)
    if temperature > 30:
        phi_ps *= 0.8
    elif temperature < 20:
        phi_ps *= 0.9
    
    # ضمان أن القيمة ضمن النطاق
    if phi_ps < 0:
        phi_ps = 0
    if phi_ps > 0.8:
        phi_ps = 0.8
    
    if return_full:
        return {
            'phi_ps': phi_ps,
            'f_v': f_v,
            'f_m': f_m,
            'f_0': f_0,
            'status': quantum_yield_status(phi_ps)
        }
    
    return phi_ps


def quantum_yield_status(phi_ps: float) -> str:
    """
    Classify photosynthetic health status.
    
    Parameters
    ----------
    phi_ps : float
        Quantum yield
    
    Returns
    -------
    str
        Health status
    """
    if phi_ps >= QUANTUM_YIELD_THRESHOLDS['optimal_min']:
        return 'optimal'
    elif phi_ps >= QUANTUM_YIELD_THRESHOLDS['photoinhibition_max']:
        return 'healthy'
    elif phi_ps >= QUANTUM_YIELD_THRESHOLDS['bleaching_max']:
        return 'stressed'
    else:
        return 'bleaching'


def electron_transport_rate(phi_ps: float, light_intensity: float) -> float:
    """
    Calculate electron transport rate.
    
    Parameters
    ----------
    phi_ps : float
        Quantum yield
    light_intensity : float
        Light intensity (μmol photons m⁻² s⁻¹)
    
    Returns
    -------
    float
        Electron transport rate
    """
    return phi_ps * light_intensity * 0.84 * 0.5


def bleaching_risk_from_yield(phi_ps: float, duration_days: int, temperature_anomaly: float) -> dict:
    """
    Calculate bleaching risk.
    
    Parameters
    ----------
    phi_ps : float
        Quantum yield
    duration_days : int
        Duration of stress
    temperature_anomaly : float
        Temperature anomaly
    
    Returns
    -------
    dict
        Risk assessment
    """
    if phi_ps > 0.4:
        return {'risk': 'LOW', 'probability': 0.1}
    elif phi_ps > 0.25:
        return {'risk': 'MODERATE', 'probability': 0.5}
    else:
        return {'risk': 'HIGH', 'probability': 0.9}
