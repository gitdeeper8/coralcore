# 🪸 CORAL-CORE Pytest Configuration
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""Pytest configuration and shared fixtures."""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

from coralcore.rhi.composite import ReefHealthIndex
from coralcore.parameters.calcification import CALCIFICATION_CONSTANTS
from coralcore.parameters.wave_dissipation import FRICTION_COEFFICIENTS


# =============================================================================
# FIXTURES - SAMPLE DATA
# =============================================================================

@pytest.fixture
def sample_parameters() -> dict:
    """Sample parameter values for a healthy reef."""
    return {
        'g_ca': 1.84,
        'e_diss': 91.0,
        'phi_ps': 0.67,
        'rho_skel': 1.62,
        'delta_ph': 0.08,
        's_reef': 4.3,
        'k_s': 0.15,
        't_thr': 31.2
    }


@pytest.fixture
def stressed_parameters() -> dict:
    """Sample parameter values for a stressed reef."""
    return {
        'g_ca': 0.65,
        'e_diss': 72.0,
        'phi_ps': 0.38,
        'rho_skel': 1.25,
        'delta_ph': 0.14,
        's_reef': 3.2,
        'k_s': 0.08,
        't_thr': 29.8
    }


@pytest.fixture
def critical_parameters() -> dict:
    """Sample parameter values for a critically degraded reef."""
    return {
        'g_ca': 0.21,
        'e_diss': 45.0,
        'phi_ps': 0.18,
        'rho_skel': 0.92,
        'delta_ph': 0.22,
        's_reef': 2.1,
        'k_s': 0.03,
        't_thr': 28.5
    }


@pytest.fixture
def sample_timeseries() -> pd.DataFrame:
    """Generate sample time series data."""
    dates = pd.date_range(start='2025-01-01', periods=100, freq='D')
    
    np.random.seed(42)
    data = {
        'timestamp': dates,
        'g_ca': 1.5 + 0.5 * np.random.randn(100).cumsum() * 0.1,
        'e_diss': 80 + 10 * np.random.randn(100).cumsum() * 0.1,
        'phi_ps': 0.6 + 0.1 * np.random.randn(100).cumsum() * 0.1,
        'rho_skel': 1.4 + 0.2 * np.random.randn(100).cumsum() * 0.1,
        'delta_ph': 0.1 + 0.02 * np.random.randn(100).cumsum() * 0.1,
        's_reef': 3.8 + 0.5 * np.random.randn(100).cumsum() * 0.1,
        'k_s': 0.12 + 0.03 * np.random.randn(100).cumsum() * 0.1,
        't_thr': 30.5 + 1.0 * np.random.randn(100).cumsum() * 0.1,
        'bleaching_event': np.random.choice([0, 1], 100, p=[0.9, 0.1])
    }
    
    return pd.DataFrame(data)


@pytest.fixture
def sample_acoustic() -> np.ndarray:
    """Generate sample acoustic signal."""
    np.random.seed(42)
    duration = 10.0  # seconds
    sr = 96000  # Hz
    t = np.linspace(0, duration, int(sr * duration))
    
    # Fish chorus (400-800 Hz)
    fish = 0.5 * np.sin(2 * np.pi * 500 * t)
    
    # Snapping shrimp (2000-5000 Hz)
    shrimp = 0.3 * np.sin(2 * np.pi * 3000 * t)
    
    # Background noise
    noise = 0.1 * np.random.randn(len(t))
    
    return fish + shrimp + noise


@pytest.fixture
def sample_elevation() -> np.ndarray:
    """Generate sample elevation data for roughness calculation."""
    np.random.seed(42)
    size = 200
    x, y = np.meshgrid(np.linspace(0, 1, size), np.linspace(0, 1, size))
    
    # Create rough surface
    z = (np.sin(10 * x) * np.cos(10 * y) + 
         0.5 * np.sin(20 * x) * np.cos(20 * y) +
         0.2 * np.random.randn(size, size))
    
    return z


@pytest.fixture
def rhi_calculator():
    """Return initialized RHI calculator."""
    return ReefHealthIndex()


@pytest.fixture
def data_dir() -> Path:
    """Return path to test data directory."""
    return Path(__file__).parent / 'data'


# =============================================================================
# FIXTURES - MOCK SENSORS
# =============================================================================

class MockSAMISensor:
    """Mock SAMI-alk sensor for testing."""
    
    def __init__(self, port='/dev/ttyUSB0'):
        self.port = port
        self.connected = True
    
    def read(self):
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'ph': 8.1 + 0.05 * np.random.randn(),
            'alkalinity': 2300 + 50 * np.random.randn(),
            'temperature': 28.0 + 0.5 * np.random.randn()
        }


class MockAMARSensor:
    """Mock AMAR G4 acoustic sensor for testing."""
    
    def __init__(self, mount='/mnt/amar'):
        self.mount = mount
        self.connected = True
    
    def read(self, duration=10):
        sr = 96000
        t = np.linspace(0, duration, int(sr * duration))
        data = 0.5 * np.sin(2 * np.pi * 500 * t) + 0.1 * np.random.randn(len(t))
        return data, sr


@pytest.fixture
def mock_sami():
    """Return mock SAMI sensor."""
    return MockSAMISensor()


@pytest.fixture
def mock_amar():
    """Return mock AMAR sensor."""
    return MockAMARSensor()


# =============================================================================
# FIXTURES - DATABASE
# =============================================================================

@pytest.fixture
def db_connection_string():
    """Return test database connection string."""
    return "sqlite:///:memory:"


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50],
        'C': ['x', 'y', 'z', 'w', 'v']
    })
