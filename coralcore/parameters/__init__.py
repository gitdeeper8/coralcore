# 🪸 CORAL-CORE Parameters Module
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""
CORAL-CORE Eight-Parameter Framework
====================================

The framework characterizes reef function through eight critical
biophysical parameters spanning five physical domains:

1. Calcification Rate (G_ca) - Physical Chemistry
2. Wave Energy Dissipation (E_diss) - Fluid Mechanics
3. Zooxanthellae Quantum Yield (Φ_ps) - Quantum Biology
4. Skeletal Bulk Density (ρ_skel) - Materials Science
5. Ocean Acidification Lag (ΔpH) - Marine Chemistry
6. Acoustic Reef Signature (S_reef) - Acoustics
7. Surface Roughness Index (k_s) - Hydraulics
8. Thermal Bleaching Threshold (T_thr) - Thermodynamics
"""

from coralcore.parameters.calcification import (
    calcification_rate,
    get_species_constant,
    CALCIFICATION_CONSTANTS
)

from coralcore.parameters.wave_dissipation import (
    wave_energy_dissipation,
    friction_coefficient,
    WAVE_CONSTANTS
)

from coralcore.parameters.quantum_yield import (
    quantum_yield,
    quantum_yield_status,
    PHOTOSYNTHESIS_THRESHOLDS
)

from coralcore.parameters.skeletal_density import (
    skeletal_density,
    stress_strain_relationship,
    DENSITY_CONSTANTS
)

from coralcore.parameters.acidification_lag import (
    acidification_lag,
    ph_upregulation_cost,
    ACIDIFICATION_CONSTANTS
)

from coralcore.parameters.acoustic_signature import (
    acoustic_signature,
    spectral_decomposition,
    ACOUSTIC_BANDS
)

from coralcore.parameters.surface_roughness import (
    surface_roughness,
    nikurade_colebrook,
    ROUGHNESS_CONSTANTS
)

from coralcore.parameters.bleaching_threshold import (
    thermal_bleaching_threshold,
    bleaching_risk,
    THERMAL_CONSTANTS
)

__all__ = [
    # Calcification
    'calcification_rate',
    'get_species_constant',
    'CALCIFICATION_CONSTANTS',
    
    # Wave dissipation
    'wave_energy_dissipation',
    'friction_coefficient',
    'WAVE_CONSTANTS',
    
    # Quantum yield
    'quantum_yield',
    'quantum_yield_status',
    'PHOTOSYNTHESIS_THRESHOLDS',
    
    # Skeletal density
    'skeletal_density',
    'stress_strain_relationship',
    'DENSITY_CONSTANTS',
    
    # Acidification lag
    'acidification_lag',
    'ph_upregulation_cost',
    'ACIDIFICATION_CONSTANTS',
    
    # Acoustic signature
    'acoustic_signature',
    'spectral_decomposition',
    'ACOUSTIC_BANDS',
    
    # Surface roughness
    'surface_roughness',
    'nikurade_colebrook',
    'ROUGHNESS_CONSTANTS',
    
    # Thermal threshold
    'thermal_bleaching_threshold',
    'bleaching_risk',
    'THERMAL_CONSTANTS'
]

__version__ = '1.0.0'
__doi__ = '10.5281/zenodo.18913829'
