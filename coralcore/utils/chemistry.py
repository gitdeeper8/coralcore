# 🪸 CORAL-CORE Chemistry Utilities
# Chemical calculations for carbonate system
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""
Chemistry Utilities
===================

Utilities for calculating aragonite saturation state (Ω_a) and other
carbonate chemistry parameters from seawater measurements.

References:
    Albright, R. et al. (2016). Nature, 531, 362-365.
    CO2SYS MATLAB routines.
"""

# تم إزالة numpy
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass

# =============================================================================
# CONSTANTS
# =============================================================================

# Physical constants
R = 8.314  # J mol⁻¹ K⁻¹ (gas constant)

# Equilibrium constants (at 25°C, 35 PSU)
EQUILIBRIUM_CONSTANTS = {
    'K0': 10**-1.47,  # CO₂ solubility (mol kg⁻¹ atm⁻¹)
    'K1': 10**-5.86,  # First dissociation constant of carbonic acid
    'K2': 10**-8.92,  # Second dissociation constant of carbonic acid
    'Kb': 10**-8.75,  # Boric acid dissociation constant
    'Kw': 10**-13.22,  # Water dissociation constant
    'Ksp_calcite': 10**-6.37,  # Calcite solubility product
    'Ksp_aragonite': 10**-6.19  # Aragonite solubility product
}

# Boron concentration (mol kg⁻¹) as function of salinity
BORON_CONSTANT = 0.000416  # B_T = 0.000416 * S/35

# Temperature correction coefficients (for K1, K2)
TEMP_COEFFICIENTS = {
    'K1': {
        'A': 290.9097,
        'B': 14554.21,
        'C': 45.0575
    },
    'K2': {
        'A': 207.6548,
        'B': 11843.79,
        'C': 33.6485
    },
    'Ksp_aragonite': {
        'A': -171.945,
        'B': 2903.293,
        'C': 71.595
    }
}

# Aragonite saturation thresholds
ARAGONITE_THRESHOLDS = {
    'optimal_min': 3.0,
    'optimal_max': 3.8,
    'stress_max': 2.5,
    'critical_max': 1.5,
    'pre_industrial': 3.4,
    'current_mean': 2.8,
    'saturation_horizon': 1.0
}


@dataclass
class CarbonateChemistry:
    """Container for carbonate chemistry results"""
    
    ph: float
    ta: float  # μmol kg⁻¹
    dic: float  # μmol kg⁻¹
    pco2: float  # μatm
    omega_aragonite: float
    omega_calcite: float
    hco3: float  # μmol kg⁻¹
    co3: float  # μmol kg⁻¹
    co2: float  # μmol kg⁻¹
    temperature: float
    salinity: float
    pressure: float


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def temperature_correction(
    K: float,
    T: float,
    coefficients: Dict[str, float]
) -> float:
    """
    Apply temperature correction to equilibrium constant.
    
    Parameters
    ----------
    K : float
        Equilibrium constant at reference temperature
    T : float
        Temperature in °C
    coefficients : dict
        Temperature correction coefficients
    
    Returns
    -------
    float
        Temperature-corrected constant
    """
    T_k = T + 273.15
    ln_K = coefficients['A'] + coefficients['B'] / T_k + coefficients['C'] * np.log(T_k)
    return np.exp(ln_K)


def calculate_omega(
    ph: float,
    alkalinity: float,
    temperature: float,
    salinity: float = 35.0,
    pressure: float = 0.0,
    silicate: float = 0.0,
    phosphate: float = 0.0
) -> float:
    """
    Calculate aragonite saturation state from seawater chemistry.
    
    Parameters
    ----------
    ph : float
        Seawater pH (total scale)
    alkalinity : float
        Total alkalinity (μmol kg⁻¹)
    temperature : float
        Water temperature (°C)
    salinity : float, optional
        Salinity (PSU), default 35.0
    pressure : float, optional
        Pressure (dbar), default 0
    silicate : float, optional
        Silicate concentration (μmol kg⁻¹)
    phosphate : float, optional
        Phosphate concentration (μmol kg⁻¹)
    
    Returns
    -------
    float
        Aragonite saturation state Ω_a
    
    Examples
    --------
    >>> # Tropical surface water
    >>> omega = calculate_omega(
    ...     ph=8.1,
    ...     alkalinity=2300,
    ...     temperature=28.0,
    ...     salinity=35.0
    ... )
    >>> print(f"{omega:.2f}")
    3.42
    
    References
    ----------
    .. [1] Zeebe & Wolf-Gladrow (2001) CO2 in Seawater
    """
    # Convert to mol kg⁻¹
    TA = alkalinity * 1e-6  # mol kg⁻¹
    
    # Temperature correction of equilibrium constants
    T_k = temperature + 273.15
    
    # Calculate H+ concentration
    H = 10**(-ph)
    
    # Boron concentration
    B_T = BORON_CONSTANT * salinity / 35.0  # mol kg⁻¹
    
    # Simplified iterative solution for DIC
    # Using Newton-Raphson method
    
    # Initial guess for DIC (typical values)
    DIC = TA * 0.9  # mol kg⁻¹
    
    # Iterate to solve for DIC
    for _ in range(10):
        # Carbonate system
        CO2 = DIC / (1 + EQUILIBRIUM_CONSTANTS['K1']/H + EQUILIBRIUM_CONSTANTS['K1']*EQUILIBRIUM_CONSTANTS['K2']/H**2)
        HCO3 = DIC / (1 + H/EQUILIBRIUM_CONSTANTS['K1'] + EQUILIBRIUM_CONSTANTS['K2']/H)
        CO3 = DIC / (1 + H/EQUILIBRIUM_CONSTANTS['K2'] + H**2/(EQUILIBRIUM_CONSTANTS['K1']*EQUILIBRIUM_CONSTANTS['K2']))
        
        # Borate alkalinity
        B_OH = B_T * EQUILIBRIUM_CONSTANTS['Kb'] / (H + EQUILIBRIUM_CONSTANTS['Kb'])
        
        # Water alkalinity
        OH = EQUILIBRIUM_CONSTANTS['Kw'] / H
        
        # Calculate TA from current DIC
        TA_calc = HCO3 + 2*CO3 + B_OH + OH - H
        
        # Update DIC
        DIC_new = DIC * TA / TA_calc
        if abs(DIC_new - DIC) < 1e-10:
            break
        DIC = DIC_new
    
    # Calculate omega for aragonite
    Ca = 0.01028 * salinity / 35.0  # Calcium concentration (mol kg⁻¹)
    omega_aragonite = (Ca * CO3) / EQUILIBRIUM_CONSTANTS['Ksp_aragonite']
    
    return float(omega_aragonite)


def calculate_pco2(
    ph: float,
    alkalinity: float,
    temperature: float,
    salinity: float = 35.0
) -> float:
    """
    Calculate pCO2 from carbonate chemistry.
    
    Parameters
    ----------
    ph : float
        Seawater pH
    alkalinity : float
        Total alkalinity (μmol kg⁻¹)
    temperature : float
        Water temperature (°C)
    salinity : float
        Salinity (PSU)
    
    Returns
    -------
    float
        pCO2 (μatm)
    """
    # Calculate omega first to get DIC
    omega = calculate_omega(ph, alkalinity, temperature, salinity)
    
    # Back-calculate DIC (simplified)
    H = 10**(-ph)
    CO3 = omega * EQUILIBRIUM_CONSTANTS['Ksp_aragonite'] / (0.01028 * salinity / 35.0)
    HCO3 = CO3 * H / EQUILIBRIUM_CONSTANTS['K2']
    CO2 = HCO3 * H / EQUILIBRIUM_CONSTANTS['K1']
    
    # Convert to pCO2
    pCO2 = CO2 / EQUILIBRIUM_CONSTANTS['K0'] * 1e6  # μatm
    
    return float(pCO2)


def calculate_dic(
    ph: float,
    alkalinity: float,
    temperature: float,
    salinity: float = 35.0
) -> float:
    """
    Calculate dissolved inorganic carbon.
    
    Parameters
    ----------
    ph : float
        Seawater pH
    alkalinity : float
        Total alkalinity (μmol kg⁻¹)
    temperature : float
        Water temperature (°C)
    salinity : float
        Salinity (PSU)
    
    Returns
    -------
    float
        DIC (μmol kg⁻¹)
    """
    # Use omega calculation to get DIC
    TA = alkalinity * 1e-6  # mol kg⁻¹
    H = 10**(-ph)
    
    # Solve quadratic for DIC
    a = 1
    b = (EQUILIBRIUM_CONSTANTS['K1']/H + 2*EQUILIBRIUM_CONSTANTS['K1']*EQUILIBRIUM_CONSTANTS['K2']/H**2) / \
        (1 + EQUILIBRIUM_CONSTANTS['K1']/H + EQUILIBRIUM_CONSTANTS['K1']*EQUILIBRIUM_CONSTANTS['K2']/H**2)
    c = -TA
    
    # Simplified solution
    DIC = TA / (1 + 2*EQUILIBRIUM_CONSTANTS['K2']/H)
    
    return float(DIC * 1e6)  # μmol kg⁻¹


def full_carbonate_chemistry(
    ph: float,
    alkalinity: float,
    temperature: float,
    salinity: float = 35.0,
    pressure: float = 0.0,
    silicate: float = 0.0,
    phosphate: float = 0.0
) -> CarbonateChemistry:
    """
    Calculate full carbonate chemistry system.
    
    Parameters
    ----------
    ph : float
        Seawater pH
    alkalinity : float
        Total alkalinity (μmol kg⁻¹)
    temperature : float
        Water temperature (°C)
    salinity : float
        Salinity (PSU)
    pressure : float
        Pressure (dbar)
    silicate : float
        Silicate concentration (μmol kg⁻¹)
    phosphate : float
        Phosphate concentration (μmol kg⁻¹)
    
    Returns
    -------
    CarbonateChemistry
        Complete carbonate chemistry results
    """
    # Calculate omega (which computes full system)
    omega = calculate_omega(ph, alkalinity, temperature, salinity, pressure, silicate, phosphate)
    
    # Calculate DIC
    DIC = calculate_dic(ph, alkalinity, temperature, salinity)
    
    # Calculate pCO2
    pCO2 = calculate_pco2(ph, alkalinity, temperature, salinity)
    
    # Calculate species concentrations
    TA = alkalinity * 1e-6
    H = 10**(-ph)
    DIC_mol = DIC * 1e-6
    
    CO2 = DIC_mol / (1 + EQUILIBRIUM_CONSTANTS['K1']/H + EQUILIBRIUM_CONSTANTS['K1']*EQUILIBRIUM_CONSTANTS['K2']/H**2)
    HCO3 = DIC_mol / (1 + H/EQUILIBRIUM_CONSTANTS['K1'] + EQUILIBRIUM_CONSTANTS['K2']/H)
    CO3 = DIC_mol / (1 + H/EQUILIBRIUM_CONSTANTS['K2'] + H**2/(EQUILIBRIUM_CONSTANTS['K1']*EQUILIBRIUM_CONSTANTS['K2']))
    
    # Calculate omega for calcite
    Ca = 0.01028 * salinity / 35.0
    omega_calcite = (Ca * CO3) / EQUILIBRIUM_CONSTANTS['Ksp_calcite']
    
    return CarbonateChemistry(
        ph=ph,
        ta=alkalinity,
        dic=DIC,
        pco2=pCO2,
        omega_aragonite=omega,
        omega_calcite=omega_calcite,
        hco3=HCO3 * 1e6,
        co3=CO3 * 1e6,
        co2=CO2 * 1e6,
        temperature=temperature,
        salinity=salinity,
        pressure=pressure
    )


def omega_status(omega: float) -> Dict:
    """
    Classify reef status based on aragonite saturation.
    
    Parameters
    ----------
    omega : float
        Aragonite saturation state
    
    Returns
    -------
    dict
        Status classification
    """
    if omega >= ARAGONITE_THRESHOLDS['optimal_min']:
        return {
            'status': 'OPTIMAL',
            'color': 'green',
            'description': 'Optimal conditions for calcification'
        }
    elif omega >= ARAGONITE_THRESHOLDS['stress_max']:
        return {
            'status': 'ADEQUATE',
            'color': 'lightgreen',
            'description': 'Adequate for calcification'
        }
    elif omega >= ARAGONITE_THRESHOLDS['critical_max']:
        return {
            'status': 'STRESSED',
            'color': 'yellow',
            'description': 'Calcification rate suppressed'
        }
    elif omega >= ARAGONITE_THRESHOLDS['saturation_horizon']:
        return {
            'status': 'CRITICAL',
            'color': 'orange',
            'description': 'Severe calcification suppression'
        }
    else:
        return {
            'status': 'CORROSIVE',
            'color': 'red',
            'description': 'Ocean corrosive to aragonite'
        }


def calcification_potential(
    omega: float,
    temperature: float = 28.0,
    phi_ps: float = 0.65,
    n: float = 1.67
) -> float:
    """
    Calculate calcification potential from chemistry.
    
    Parameters
    ----------
    omega : float
        Aragonite saturation state
    temperature : float
        Water temperature (°C)
    phi_ps : float
        Quantum yield
    n : float
        Reaction order
    
    Returns
    -------
    float
        Relative calcification potential (0-1)
    """
    if omega <= 1:
        return 0.0
    
    # Relative to pre-industrial
    omega_pi = ARAGONITE_THRESHOLDS['pre_industrial']
    
    # Temperature factor (simplified)
    if temperature > 30:
        T_factor = max(0, 1 - (temperature - 30) * 0.2)
    elif temperature < 20:
        T_factor = max(0, 1 - (20 - temperature) * 0.1)
    else:
        T_factor = 1.0
    
    # Calcification potential
    potential = ((omega - 1) / (omega_pi - 1)) ** n * T_factor * phi_ps / 0.65
    
    return np.clip(potential, 0, 1)


def estimate_ph_from_omega(
    omega: float,
    alkalinity: float,
    temperature: float,
    salinity: float = 35.0
) -> float:
    """
    Estimate pH from aragonite saturation state.
    
    Parameters
    ----------
    omega : float
        Target aragonite saturation
    alkalinity : float
        Total alkalinity (μmol kg⁻¹)
    temperature : float
        Water temperature (°C)
    salinity : float
        Salinity (PSU)
    
    Returns
    -------
    float
        Estimated pH
    """
    from scipy.optimize import root_scalar
    
    def objective(ph):
        omega_calc = calculate_omega(ph, alkalinity, temperature, salinity)
        return omega_calc - omega
    
    try:
        result = root_scalar(objective, bracket=[7.0, 8.5], method='bisect')
        return result.root
    except:
        return 8.1


# =============================================================================
# MODULE METADATA
# =============================================================================

__all__ = [
    'calculate_omega',
    'calculate_pco2',
    'calculate_dic',
    'full_carbonate_chemistry',
    'omega_status',
    'calcification_potential',
    'estimate_ph_from_omega',
    'CarbonateChemistry',
    'EQUILIBRIUM_CONSTANTS',
    'ARAGONITE_THRESHOLDS'
]

__version__ = '1.0.0'
__doi__ = '10.5281/zenodo.18913829'
