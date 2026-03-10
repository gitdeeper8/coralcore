# 🪸 CORAL-CORE Acoustics Tests
# Unit tests for acoustics utilities
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Unit tests for acoustics utilities."""

import pytest
import numpy as np
from coralcore.utils.acoustics import (
    compute_spectrogram,
    extract_features,
    detect_snapping_shrimp,
    design_restoration_signal,
    calculate_sound_pressure_level,
    compute_aci,
    compute_bi,
    compute_ndsi
)


class TestAcoustics:
    """Test suite for acoustics utilities."""
    
    def test_compute_spectrogram(self, sample_acoustic):
        """Test spectrogram computation."""
        S_db, freqs, times = compute_spectrogram(sample_acoustic, sr=96000)
        
        assert S_db.shape[0] == len(freqs)
        assert S_db.shape[1] == len(times)
        assert freqs[0] >= 0
        assert times[0] >= 0
    
    def test_extract_features(self, sample_acoustic):
        """Test feature extraction."""
        features = extract_features(sample_acoustic, sr=96000)
        
        assert features.shannon_entropy > 0
        assert features.spectral_centroid > 0
        assert features.spectral_bandwidth > 0
        assert features.zero_crossing_rate > 0
        assert len(features.mfccs) == 13
        assert len(features.band_powers) > 0
    
    def test_detect_snapping_shrimp(self, sample_acoustic):
        """Test snapping shrimp detection."""
        # Add some shrimp-like pulses
        sr = 96000
        audio = sample_acoustic.copy()
        
        # Add pulses
        for i in range(10):
            idx = i * sr
            if idx + 100 < len(audio):
                audio[idx:idx+100] += 1.0
        
        result = detect_snapping_shrimp(audio, sr=sr)
        
        assert 'snap_count' in result
        assert 'snap_rate' in result
        assert 'activity_level' in result
    
    def test_design_restoration_signal(self):
        """Test restoration signal design."""
        signal = design_restoration_signal(
            duration=5.0,
            sr=96000,
            target_bands=['fish_chorus', 'snapping_shrimp']
        )
        
        assert len(signal) == 5 * 96000
        assert np.max(np.abs(signal)) <= 1.0
        assert np.min(signal) >= -1.0
    
    def test_calculate_spl(self, sample_acoustic):
        """Test sound pressure level calculation."""
        spl = calculate_sound_pressure_level(sample_acoustic)
        
        assert spl > 0
        assert isinstance(spl, float)
    
    def test_compute_aci(self, sample_acoustic):
        """Test Acoustic Complexity Index."""
        S_db, freqs, times = compute_spectrogram(sample_acoustic)
        S_power = 10 ** (S_db / 10)
        
        aci = compute_aci(S_power)
        
        assert aci > 0
        assert isinstance(aci, float)
    
    def test_compute_bi(self):
        """Test Biodiversity Index."""
        band_powers = {
            'fish_chorus': 80,
            'invertebrate': 75,
            'snapping_shrimp': 70,
            'low': 50
        }
        
        bi = compute_bi(band_powers)
        
        assert 0 <= bi <= 1
        assert bi > 0
    
    def test_compute_ndsi(self):
        """Test Normalized Difference Soundscape Index."""
        band_powers = {
            'fish_chorus': 80,
            'low': 50
        }
        
        ndsi = compute_ndsi(band_powers)
        
        assert -1 <= ndsi <= 1
        assert ndsi > 0  # Biophony dominates
    
    def test_band_powers(self, sample_acoustic):
        """Test band power extraction."""
        features = extract_features(sample_acoustic)
        
        assert 'fish_chorus' in features.band_powers
        assert 'snapping_shrimp' in features.band_powers
        assert 'low' in features.band_powers
    
    def test_mfcc_consistency(self, sample_acoustic):
        """Test MFCC consistency."""
        features1 = extract_features(sample_acoustic[:len(sample_acoustic)//2])
        features2 = extract_features(sample_acoustic)
        
        # MFCCs should be reasonably similar
        assert np.mean(np.abs(features1.mfccs - features2.mfccs[:13])) < 10
