# 🪸 CORAL-CORE Calcification Rate Module (Pure Python)
# Version: 1.0.0 - بدون أي إشارة إلى numpy

"""
Calcification Rate Module - Pure Python implementation
"""

# =============================================================================
# CONSTANTS
# =============================================================================

CALCIFICATION_CONSTANTS = {
    'acropora_millepora': {
        'k': 2.14,
        'n': 1.67,
        'description': 'Branching Acropora, fast-growing'
    },
    'porites_lobata': {
        'k': 0.31,
        'n': 1.67,
        'description': 'Massive Porites, slow-growing'
    },
    'default': {
        'k': 1.00,
        'n': 1.67,
        'description': 'Default values'
    }
}


def calcification_rate(
    omega_a=3.4,
    phi_ps=0.65,
    temperature=28.0,
    t_thr=31.5,
    species='acropora_millepora',
    k_value=None,
    n_value=None,
    return_full=False
):
    """
    Calculate calcification rate - Pure Python.
    """
    if omega_a <= 1.0:
        return 0.0
    
    # اختيار الثابت من المعطيات أو من الثوابت
    if k_value is not None:
        k = k_value
    else:
        k = CALCIFICATION_CONSTANTS.get(species, CALCIFICATION_CONSTANTS['default'])['k']
    
    # عامل درجة الحرارة
    if temperature >= t_thr:
        f_t = 0.0
    elif temperature < 20:
        f_t = 0.5
    elif temperature < 28:
        f_t = 0.8
    else:
        f_t = 1.0
    
    # حساب المعدل
    rate = k * (omega_a - 1) * f_t * phi_ps
    
    # ضبط النطاق
    if rate < 0:
        rate = 0
    if rate > 5:
        rate = 5
    
    if return_full:
        return {
            'rate': rate,
            'omega_a': omega_a,
            'k': k,
            'temperature_factor': f_t,
            'phi_ps': phi_ps,
            'species': species
        }
    
    return rate


def get_species_constant(species):
    """Get species constant."""
    return CALCIFICATION_CONSTANTS.get(
        species, CALCIFICATION_CONSTANTS['default']
    ).copy()


# تصدير الثوابت للاستخدام في وحدات أخرى
__all__ = ['calcification_rate', 'get_species_constant', 'CALCIFICATION_CONSTANTS']
