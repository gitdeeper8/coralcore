# 🪸 CORAL-CORE RHI Tests
# Unit tests for Reef Health Index module
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Unit tests for Reef Health Index calculations."""

import pytest
import numpy as np
from coralcore.rhi.composite import ReefHealthIndex, RHIResult
from coralcore.rhi.weights import PCA_WEIGHTS


class TestReefHealthIndex:
    """Test suite for Reef Health Index."""
    
    def test_rhi_healthy(self, sample_parameters, rhi_calculator):
        """Test RHI for healthy reef."""
        result = rhi_calculator.compute(
            sample_parameters,
            station_id='TEST001',
            return_full=True
        )
        
        assert result.rhi >= 0.8
        assert result.status == 'HEALTHY'
        assert result.color == '🟢'
        assert len(result.normalized_params) == 8
        assert len(result.contributions) == 8
    
    def test_rhi_stressed(self, stressed_parameters, rhi_calculator):
        """Test RHI for stressed reef."""
        result = rhi_calculator.compute(
            stressed_parameters,
            return_full=True
        )
        
        assert 0.5 <= result.rhi < 0.8
        assert result.status == 'STRESSED'
    
    def test_rhi_critical(self, critical_parameters, rhi_calculator):
        """Test RHI for critically degraded reef."""
        result = rhi_calculator.compute(
            critical_parameters,
            return_full=True
        )
        
        assert result.rhi < 0.5
        assert result.status == 'CRITICAL'
    
    def test_rhi_return_float(self, sample_parameters, rhi_calculator):
        """Test RHI returning float only."""
        rhi = rhi_calculator.compute(
            sample_parameters,
            return_full=False
        )
        
        assert isinstance(rhi, float)
        assert 0 <= rhi <= 1
    
    def test_missing_parameter(self, sample_parameters, rhi_calculator):
        """Test missing parameter raises error."""
        incomplete = sample_parameters.copy()
        del incomplete['g_ca']
        
        with pytest.raises(ValueError):
            rhi_calculator.compute(incomplete)
    
    def test_weights_sum_to_one(self):
        """Test that weights sum to 1.0."""
        total = sum(PCA_WEIGHTS.values())
        assert total == pytest.approx(1.0, rel=1e-6)
    
    def test_custom_weights(self, sample_parameters):
        """Test custom weights."""
        custom_weights = {
            'g_ca': 0.5,
            'e_diss': 0.1,
            'phi_ps': 0.1,
            'rho_skel': 0.1,
            'delta_ph': 0.05,
            's_reef': 0.05,
            'k_s': 0.05,
            't_thr': 0.05
        }
        
        rhi_calc = ReefHealthIndex(weights=custom_weights)
        result = rhi_calc.compute(sample_parameters, return_full=True)
        
        assert result.rhi > 0
        assert abs(sum(result.contributions.values()) - result.rhi) < 1e-6
    
    def test_normalization(self, rhi_calculator):
        """Test parameter normalization."""
        # Test extreme values
        params = {
            'g_ca': 0.0,
            'e_diss': 0.0,
            'phi_ps': 0.0,
            'rho_skel': 0.5,
            'delta_ph': 0.25,
            's_reef': 2.0,
            'k_s': 0.0,
            't_thr': 28.0
        }
        
        rhi = rhi_calculator.compute(params, return_full=False)
        assert rhi >= 0
        
        # Test maximum values
        params = {
            'g_ca': 2.5,
            'e_diss': 100.0,
            'phi_ps': 0.8,
            'rho_skel': 2.0,
            'delta_ph': 0.0,
            's_reef': 5.0,
            'k_s': 0.35,
            't_thr': 34.0
        }
        
        rhi = rhi_calculator.compute(params, return_full=False)
        assert rhi <= 1.0
    
    def test_trend_calculation(self, sample_parameters, rhi_calculator):
        """Test RHI trend calculation."""
        # First calculation
        rhi_calculator.compute(sample_parameters, station_id='TEST001')
        
        # Second calculation (slightly different)
        params2 = sample_parameters.copy()
        params2['g_ca'] *= 0.95
        result = rhi_calculator.compute(params2, return_full=True)
        
        assert result.trend is not None
    
    def test_history(self, sample_parameters, rhi_calculator):
        """Test history storage."""
        for i in range(5):
            params = sample_parameters.copy()
            params['g_ca'] *= (1 + i * 0.01)
            rhi_calculator.compute(params, station_id='TEST001')
        
        assert len(rhi_calculator.history) == 5
        assert rhi_calculator.history[0]['station_id'] == 'TEST001'
    
    def test_get_trend(self, sample_parameters, rhi_calculator):
        """Test trend analysis."""
        for i in range(30):
            params = sample_parameters.copy()
            params['g_ca'] *= (1 - i * 0.005)
            rhi_calculator.compute(params)
        
        trend = rhi_calculator.get_trend(days=30)
        assert 'direction' in trend
        assert 'rate' in trend
        assert 'change_percent' in trend
    
    def test_check_alerts(self, sample_parameters, rhi_calculator):
        """Test alert checking."""
        # Add some critical values
        critical = sample_parameters.copy()
        critical['phi_ps'] = 0.2
        rhi_calculator.compute(critical)
        
        alerts = rhi_calculator.check_alerts(threshold=0.5)
        assert len(alerts) > 0
        assert alerts[0]['severity'] == 'CRITICAL'
