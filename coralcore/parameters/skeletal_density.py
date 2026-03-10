# 🪸 CORAL-CORE Skeletal Density Module (Pure Python)
# Version: 1.0.0 - نسخة مبسطة للغاية

"""
Skeletal Bulk Density Module - Pure Python implementation
"""

# =============================================================================
# CONSTANTS
# =============================================================================

DENSITY_CONSTANTS = {
    'aragonite_density': 2.93,  # g/cm³
    'youngs_modulus': 80e9,  # Pa
    'density_ranges': {
        'branching': {'min': 0.8, 'max': 1.2, 'typical': 1.0},
        'massive': {'min': 1.4, 'max': 1.85, 'typical': 1.6},
        'encrusting': {'min': 1.2, 'max': 1.6, 'typical': 1.4}
    }
}

DENSITY_THRESHOLDS = {
    'healthy_min_branching': 1.0,
    'healthy_min_massive': 1.5,
    'critical_max_branching': 0.8,
    'critical_max_massive': 1.2
}


def skeletal_density(
    dry_weight: float = 100.0,
    volume: float = 100.0,
    morphology: str = 'massive',
    return_full: bool = False
) -> float:
    """
    Calculate skeletal bulk density.
    
    Parameters
    ----------
    dry_weight : float
        Dry weight in grams
    volume : float
        Bulk volume in cm³
    morphology : str
        Coral morphology
    return_full : bool
        Return full result
    
    Returns
    -------
    float
        Bulk density in g/cm³
    """
    if volume <= 0:
        return 0.0
    
    density = dry_weight / volume
    
    if return_full:
        density_ratio = density / DENSITY_CONSTANTS['aragonite_density']
        return {
            'density': density,
            'morphology': morphology,
            'porosity': 1 - density_ratio,
            'density_ratio': density_ratio,
            'status': density_status(density, morphology)
        }
    
    return density


def density_status(density: float, morphology: str = 'massive') -> str:
    """
    Classify mechanical integrity status.
    
    Parameters
    ----------
    density : float
        Bulk density
    morphology : str
        Coral morphology
    
    Returns
    -------
    str
        Status
    """
    if morphology in ['branching', 'tabular']:
        if density >= 1.0:
            return 'healthy'
        elif density >= 0.8:
            return 'stressed'
        else:
            return 'critical'
    else:  # massive, encrusting
        if density >= 1.5:
            return 'healthy'
        elif density >= 1.2:
            return 'stressed'
        else:
            return 'critical'


def stress_strain_relationship(
    stress: float = None,
    strain: float = None,
    density: float = 1.5
) -> dict:
    """
    Calculate stress-strain relationship.
    
    Parameters
    ----------
    stress : float, optional
        Applied stress in Pa
    strain : float, optional
        Mechanical strain
    density : float
        Bulk density
    
    Returns
    -------
    dict
        Relationship results
    """
    density_ratio = density / DENSITY_CONSTANTS['aragonite_density']
    E_effective = DENSITY_CONSTANTS['youngs_modulus'] * density_ratio**2
    
    if stress is not None and strain is None:
        return {
            'stress': stress,
            'strain': stress / E_effective if E_effective > 0 else 0,
            'youngs_modulus_effective': E_effective
        }
    elif strain is not None and stress is None:
        return {
            'stress': E_effective * strain,
            'strain': strain,
            'youngs_modulus_effective': E_effective
        }
    else:
        return {'error': 'Provide either stress or strain'}


def estimate_wave_loading_limit(density: float, safety_factor: float = 2.0) -> float:
    """
    Estimate maximum wave loading.
    
    Parameters
    ----------
    density : float
        Bulk density
    safety_factor : float
        Safety factor
    
    Returns
    -------
    float
        Maximum wave height in meters
    """
    density_ratio = density / DENSITY_CONSTANTS['aragonite_density']
    sigma_max = 150e6 * density_ratio**1.5  # Pa
    sigma_allowable = sigma_max / safety_factor
    
    # Convert to wave height (تبسيط)
    wave_height = 2 * sigma_allowable / (1025 * 9.81)
    
    return wave_height
