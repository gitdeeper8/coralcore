# 🪸 CORAL-CORE Calcification Tests
# Unit tests for calcification rate module
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Unit tests for calcification rate calculations."""

import pytest
import numpy as np
from coralcore.parameters.calcification import (
    calcification_rate,
    temperature_modulation_factor,
    get_species_constant,
    CALCIFICATION_CONSTANTS
)


class TestCalcification:
    """Test suite for calcification rate module."""
    
    def test_calcification_rate_healthy(self, sample_parameters):
        """Test calcification rate for healthy reef."""
        rate = calcification_rate(
            omega_a=3.4,
            phi_ps=sample_parameters['phi_ps'],
            temperature=28.0,
            t_thr=31.5,
            species='acropora_millepora'
        )
        
        assert rate > 0
        assert rate < 2.5
        assert isinstance(rate, float)
    
    def test_calcification_rate_stressed(self):
        """Test calcification rate under stress."""
        rate = calcification_rate(
            omega_a=2.2,
            phi_ps=0.35,
            temperature=30.5,
            t_thr=31.0,
            species='acropora_millepora'
        )
        
        assert rate < 1.0
        assert rate >= 0
    
    def test_calcification_rate_below_threshold(self):
        """Test calcification rate above bleaching threshold."""
        rate = calcification_rate(
            omega_a=3.4,
            phi_ps=0.65,
            temperature=32.0,
            t_thr=31.0,
            species='acropora_millepora'
        )
        
        assert rate == 0.0
    
    def test_temperature_modulation_factor(self):
        """Test temperature modulation factor."""
        # Below threshold
        f_t = temperature_modulation_factor(28.0, 31.0)
        assert f_t > 0
        assert f_t <= 1.0
        
        # At threshold
        f_t = temperature_modulation_factor(31.0, 31.0)
        assert f_t == 0.0
        
        # Above threshold
        f_t = temperature_modulation_factor(32.0, 31.0)
        assert f_t == 0.0
    
    def test_species_constants(self):
        """Test species-specific constants."""
        for species, data in CALCIFICATION_CONSTANTS.items():
            assert 'k' in data
            assert 'n' in data
            assert 'description' in data
            assert data['k'] > 0
            assert data['n'] == 1.67
    
    def test_get_species_constant(self):
        """Test retrieving species constants."""
        acropora = get_species_constant('acropora_millepora')
        assert acropora['k'] == 2.14
        
        default = get_species_constant('unknown_species')
        assert default['k'] == 1.0
    
    def test_porites_lobata(self):
        """Test Porites lobata (slow-growing)."""
        rate = calcification_rate(
            omega_a=3.4,
            phi_ps=0.65,
            temperature=28.0,
            t_thr=31.5,
            species='porites_lobata'
        )
        
        assert rate == pytest.approx(0.31, rel=0.1)
    
    def test_invalid_phi_ps(self):
        """Test invalid quantum yield."""
        with pytest.raises(ValueError):
            calcification_rate(
                omega_a=3.4,
                phi_ps=1.5,
                temperature=28.0,
                t_thr=31.5
            )
    
    def test_return_full_result(self, sample_parameters):
        """Test returning full result object."""
        result = calcification_rate(
            omega_a=3.4,
            phi_ps=sample_parameters['phi_ps'],
            temperature=28.0,
            t_thr=31.5,
            species='acropora_millepora',
            return_full=True
        )
        
        assert hasattr(result, 'rate')
        assert hasattr(result, 'omega_a')
        assert hasattr(result, 'k_value')
        assert hasattr(result, 'n_value')
        assert hasattr(result, 'temperature_factor')
        assert hasattr(result, 'phi_ps')
        assert hasattr(result, 'species')
        assert hasattr(result, 'uncertainty')
        
        assert result.uncertainty is not None
        assert result.uncertainty > 0
