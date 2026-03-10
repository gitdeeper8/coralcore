# 🪸 CORAL-CORE Integration Tests
# Integration tests for complete data pipeline
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Integration tests for complete CORAL-CORE pipeline."""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from coralcore.parameters.calcification import calcification_rate
from coralcore.parameters.wave_dissipation import wave_energy_dissipation
from coralcore.parameters.quantum_yield import quantum_yield
from coralcore.rhi.composite import ReefHealthIndex
from coralcore.utils.chemistry import calculate_omega
from coralcore.utils.acoustics import extract_features


class TestIntegration:
    """Integration tests for complete pipeline."""
    
    @pytest.fixture
    def complete_dataset(self):
        """Generate complete dataset with all parameters."""
        np.random.seed(42)
        n_samples = 100
        
        dates = pd.date_range(start='2025-01-01', periods=n_samples, freq='D')
        
        data = []
        for i, date in enumerate(dates):
            # Base values with trends
            trend = i / n_samples
            
            # Calcification parameters
            omega = 3.0 + 0.5 * np.sin(i / 10) - 0.5 * trend
            phi_ps = 0.65 - 0.2 * trend + 0.1 * np.random.randn()
            temp = 28.0 + 2.0 * np.sin(i / 30) + 0.5 * np.random.randn()
            t_thr = 31.0 + 0.5 * np.sin(i / 20)
            
            # Calculate calcification rate
            g_ca = calcification_rate(
                omega_a=omega,
                phi_ps=max(0.1, phi_ps),
                temperature=temp,
                t_thr=t_thr,
                species='acropora_millepora'
            )
            
            # Wave parameters
            wave_height = 2.0 + 0.5 * np.random.randn()
            roughness = 0.15 - 0.05 * trend + 0.02 * np.random.randn()
            
            e_diss = wave_energy_dissipation(
                wave_height=wave_height,
                wave_period=8.0,
                water_depth=3.0,
                roughness_length=max(0.01, roughness)
            )
            
            # Other parameters
            rho_skel = 1.5 - 0.3 * trend + 0.1 * np.random.randn()
            delta_ph = 0.08 + 0.1 * trend + 0.02 * np.random.randn()
            s_reef = 4.0 - 1.0 * trend + 0.5 * np.random.randn()
            k_s = max(0.01, roughness)
            
            data.append({
                'timestamp': date,
                'g_ca': g_ca,
                'e_diss': e_diss,
                'phi_ps': phi_ps,
                'rho_skel': rho_skel,
                'delta_ph': delta_ph,
                's_reef': s_reef,
                'k_s': k_s,
                't_thr': t_thr,
                'temperature': temp,
                'omega': omega
            })
        
        return pd.DataFrame(data)
    
    def test_complete_pipeline(self, complete_dataset):
        """Test complete data pipeline from sensors to RHI."""
        rhi_calc = ReefHealthIndex()
        results = []
        
        for _, row in complete_dataset.iterrows():
            # Calculate RHI
            params = {
                'g_ca': row['g_ca'],
                'e_diss': row['e_diss'],
                'phi_ps': row['phi_ps'],
                'rho_skel': row['rho_skel'],
                'delta_ph': row['delta_ph'],
                's_reef': row['s_reef'],
                'k_s': row['k_s'],
                't_thr': row['t_thr']
            }
            
            result = rhi_calc.compute(params, return_full=True)
            results.append(result)
        
        # Check results
        rhis = [r.rhi for r in results]
        
        assert len(rhis) == len(complete_dataset)
        assert all(0 <= r <= 1 for r in rhis)
        
        # Trend should be decreasing (degradation)
        assert rhis[0] > rhis[-1]
    
    def test_parameter_correlations(self, complete_dataset):
        """Test parameter correlations match paper."""
        # Calculate correlations
        corr_matrix = complete_dataset[['g_ca', 'e_diss', 'phi_ps', 'rho_skel', 
                                        'delta_ph', 's_reef', 'k_s', 't_thr']].corr()
        
        # Check key correlations from paper
        assert corr_matrix.loc['e_diss', 'k_s'] > 0.8  # Should be ~0.91
        assert corr_matrix.loc['g_ca', 'phi_ps'] > 0.7  # Should be ~0.83
        assert corr_matrix.loc['e_diss', 'rho_skel'] > 0.7  # Should be ~0.88
    
    def test_bleaching_detection(self, complete_dataset):
        """Test bleaching event detection."""
        rhi_calc = ReefHealthIndex()
        
        # Add bleaching event
        bleaching_idx = len(complete_dataset) // 2
        complete_dataset.loc[bleaching_idx:bleaching_idx+10, 'phi_ps'] = 0.2
        
        alerts = []
        for _, row in complete_dataset.iterrows():
            params = {k: row[k] for k in rhi_calc.weights.keys()}
            rhi = rhi_calc.compute(params, return_full=False)
            
            if rhi < 0.5:
                alerts.append(True)
            else:
                alerts.append(False)
        
        # Should detect bleaching event
        assert any(alerts[bleaching_idx:bleaching_idx+10])
    
    def test_sensor_to_rhi(self, mock_sami, mock_amar):
        """Test from mock sensors to RHI."""
        # Read mock sensors
        sami_data = mock_sami.read()
        acoustic, sr = mock_amar.read(duration=5)
        
        # Process acoustic data
        features = extract_features(acoustic, sr=sr)
        
        # Calculate omega
        omega = calculate_omega(
            ph=sami_data['ph'],
            alkalinity=sami_data['alkalinity'],
            temperature=sami_data['temperature']
        )
        
        # Calculate parameters
        g_ca = calcification_rate(
            omega_a=omega,
            phi_ps=0.65,
            temperature=sami_data['temperature'],
            t_thr=31.0
        )
        
        # Create parameter dict
        params = {
            'g_ca': g_ca,
            'e_diss': 85.0,  # Default
            'phi_ps': 0.65,
            'rho_skel': 1.5,
            'delta_ph': 0.08,
            's_reef': features.shannon_entropy,
            'k_s': 0.15,
            't_thr': 31.0
        }
        
        # Calculate RHI
        rhi_calc = ReefHealthIndex()
        rhi = rhi_calc.compute(params, return_full=False)
        
        assert 0 <= rhi <= 1
