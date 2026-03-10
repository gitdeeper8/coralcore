# 🪸 CORAL-CORE Chemistry Tests
# Unit tests for chemistry utilities
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Unit tests for chemistry utilities."""

import pytest
import numpy as np
from coralcore.utils.chemistry import (
    calculate_omega,
    calculate_pco2,
    calculate_dic,
    full_carbonate_chemistry,
    omega_status,
    calcification_potential
)


class TestChemistry:
    """Test suite for chemistry utilities."""
    
    def test_calculate_omega(self):
        """Test omega calculation."""
        omega = calculate_omega(
            ph=8.1,
            alkalinity=2300,
            temperature=28.0,
            salinity=35.0
        )
        
        assert omega > 0
        assert 2.5 < omega < 4.0
    
    def test_omega_variation(self):
        """Test omega variation with pH."""
        omega_high = calculate_omega(8.3, 2300, 28.0)
        omega_low = calculate_omega(7.9, 2300, 28.0)
        
        assert omega_high > omega_low
    
    def test_calculate_pco2(self):
        """Test pCO2 calculation."""
        pco2 = calculate_pco2(8.1, 2300, 28.0)
        
        assert pco2 > 0
        assert 300 < pco2 < 500  # μatm
    
    def test_calculate_dic(self):
        """Test DIC calculation."""
        dic = calculate_dic(8.1, 2300, 28.0)
        
        assert dic > 0
        assert 1800 < dic < 2200  # μmol/kg
    
    def test_full_chemistry(self):
        """Test full carbonate chemistry."""
        chem = full_carbonate_chemistry(
            ph=8.1,
            alkalinity=2300,
            temperature=28.0,
            salinity=35.0
        )
        
        assert chem.ph == 8.1
        assert chem.ta == 2300
        assert chem.omega_aragonite > 0
        assert chem.omega_calcite > 0
        assert chem.hco3 > 0
        assert chem.co3 > 0
        assert chem.co2 > 0
    
    def test_omega_status(self):
        """Test omega status classification."""
        # Optimal
        status = omega_status(3.5)
        assert status['status'] == 'OPTIMAL'
        
        # Stressed
        status = omega_status(2.0)
        assert status['status'] == 'STRESSED'
        
        # Corrosive
        status = omega_status(0.8)
        assert status['status'] == 'CORROSIVE'
    
    def test_calcification_potential(self):
        """Test calcification potential."""
        # Optimal conditions
        potential = calcification_potential(3.4, 28.0, 0.65)
        assert potential == pytest.approx(1.0, rel=0.1)
        
        # Stressed conditions
        potential = calcification_potential(2.2, 30.0, 0.4)
        assert potential < 0.5
        
        # Below saturation
        potential = calcification_potential(0.8)
        assert potential == 0.0
    
    def test_temperature_effect(self):
        """Test temperature effect on calcification."""
        # High temperature reduces potential
        potential_hot = calcification_potential(3.0, 32.0, 0.65)
        potential_normal = calcification_potential(3.0, 28.0, 0.65)
        
        assert potential_hot < potential_normal
        
        # Cold temperature reduces potential
        potential_cold = calcification_potential(3.0, 18.0, 0.65)
        assert potential_cold < potential_normal
    
    def test_preindustrial_suppression(self):
        """Test pre-industrial suppression."""
        from coralcore.parameters.calcification import estimate_preindustrial_suppression
        
        suppression = estimate_preindustrial_suppression(2.8, 3.4)
        assert 15 < suppression < 25  # 15-25% as per paper
    
    def test_future_projection(self):
        """Test future projection."""
        from coralcore.parameters.calcification import project_future_rate
        
        future_rate = project_future_rate(1.6, 1.0)
        assert future_rate < 0.5  # 55-70% suppression
