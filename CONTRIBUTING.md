# 🤝 Contributing to CORAL-CORE

## Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework

**DOI**: 10.5281/zenodo.18913829  
**Repository**: github.com/gitdeeper8/coralcore  
**Web**: coralcore.netlify.app

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contributing to Physics Modules](#contributing-to-physics-modules)
- [Contributing to Sensor Integration](#contributing-to-sensor-integration)
- [Contributing to Documentation](#contributing-to-documentation)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)

---

## 📜 Code of Conduct

### Our Pledge
We as members, contributors, and leaders pledge to make participation in the CORAL-CORE community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at gitdeeper@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Prerequisites
```bash
# Install development dependencies
python --version  # 3.9-3.11 required
git --version     # 2.30+ recommended
docker --version  # 20.10+ for containerized development
```

Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/coralcore.git
cd coralcore

# Add upstream remote
git remote add upstream https://github.com/gitdeeper8/coralcore.git
```

Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial setup
python scripts/init_dev.py
```

Development Tools

```bash
# Code formatting
black coralcore/ tests/
isort coralcore/ tests/

# Linting
flake8 coralcore/ tests/
pylint coralcore/ tests/

# Type checking
mypy coralcore/ tests/

# Testing
pytest tests/ -v --cov=coralcore
```

---

🔄 Development Workflow

Branch Naming Convention

```
feature/    # New features (e.g., feature/acoustic-ml)
bugfix/     # Bug fixes (e.g., bugfix/sami-connection)
docs/       # Documentation (e.g., docs/api-refactor)
research/   # Research contributions (e.g., research/red-sea-2026)
sensor/     # Sensor integrations (e.g., sensor/new-ph-probe)
```

Development Process

```bash
# 1. Update your main branch
git checkout main
git pull upstream main

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... code changes ...

# 4. Run tests locally
pytest tests/ -v

# 5. Commit with conventional commit message
git add .
git commit -m "feat: add new acoustic processing module"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
```

Commit Message Convention

We follow Conventional Commits:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style (formatting, missing semi-colons)
· refactor: Code change that neither fixes bug nor adds feature
· perf: Performance improvement
· test: Adding missing tests
· chore: Changes to build process or auxiliary tools

Examples:

```
feat(acoustic): add deep learning model for species identification
fix(sensors): resolve SAMI-alk timeout issue on Raspberry Pi
docs(rhi): update threshold values based on 2025 field data
```

---

🔬 Contributing to Physics Modules

Core Physics Equations

The CORAL-CORE framework is built on eight governing equations:

```python
# coralcore/physics/calcification.py
def calculate_calcification_rate(omega_a, phi_ps, temperature, species='acropora'):
    """
    Calculate calcification rate using G = k(Ω_a - 1)^n · f(T) · Φ_ps
    
    Parameters
    ----------
    omega_a : float
        Aragonite saturation state
    phi_ps : float
        Zooxanthellae quantum yield (0-0.8)
    temperature : float
        Water temperature in °C
    species : str
        Coral species identifier
    
    Returns
    -------
    float
        Calcification rate in mmol/cm²/day
    """
    # Species-specific constants
    constants = {
        'acropora': {'k': 2.14, 'n': 1.67},
        'porites': {'k': 0.31, 'n': 1.67},
        'montipora': {'k': 1.23, 'n': 1.67},
    }
    
    k = constants[species]['k']
    n = constants[species]['n']
    
    # Temperature modulation
    t_opt = 28.0  # Optimal temperature
    t_thr = 31.0  # Bleaching threshold
    if temperature < t_thr:
        f_t = np.exp(-56000/8.314 * (1/(temperature+273.15) - 1/(t_opt+273.15)))
    else:
        f_t = 0
    
    return k * (omega_a - 1)**n * f_t * phi_ps
```

Adding New Physics Models

```python
# coralcore/physics/new_model.py
"""
Template for contributing new physics models
"""

import numpy as np
from typing import Dict, Optional
from pydantic import BaseModel, validator

class NewModelConfig(BaseModel):
    """Configuration for new physics model"""
    
    parameter1: float
    parameter2: float
    calibration_factor: Optional[float] = 1.0
    
    @validator('parameter1')
    def validate_parameter1(cls, v):
        if v < 0 or v > 100:
            raise ValueError('parameter1 must be between 0 and 100')
        return v

class NewPhysicsModel:
    """
    New physics model implementation
    
    References
    ----------
    [1] Author et al. (2026) - DOI: 10.xxxx/xxxxx
    """
    
    def __init__(self, config: Dict):
        self.config = NewModelConfig(**config)
        self.validate_against_field_data()
    
    def compute(self, input_data: np.ndarray) -> float:
        """
        Compute model output
        
        Parameters
        ----------
        input_data : np.ndarray
            Input parameters array
        
        Returns
        -------
        float
            Model output
        """
        # Implement your model here
        result = self.config.parameter1 * input_data.mean()
        return result * self.config.calibration_factor
    
    def validate_against_field_data(self):
        """Validate model against CORAL-CORE field dataset"""
        # Load validation data
        # Compare predictions with observations
        # Report validation metrics
        pass
    
    def get_references(self) -> list:
        """Return list of academic references"""
        return [
            "Author, A. et al. (2026). Title. Journal, volume, pages."
        ]
```

---

📡 Contributing to Sensor Integration

Adding New Sensor Support

```python
# coralcore/sensors/new_sensor.py
"""
Template for adding new sensor support
"""

import serial
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from coralcore.sensors.base import BaseSensor

class NewSensor(BaseSensor):
    """
    Driver for New Sensor Model X
    
    Specifications
    --------------
    - Manufacturer: SensorCo
    - Output: pH, temperature, salinity
    - Interface: RS232 / USB
    - Baud rate: 9600
    """
    
    def __init__(self, port: str, baudrate: int = 9600, **kwargs):
        super().__init__(port, baudrate, **kwargs)
        self.sensor_type = "chemical"
        self.parameters = ["ph", "temperature", "salinity"]
        self.unit_map = {
            "ph": "pH",
            "temperature": "°C",
            "salinity": "PSU"
        }
    
    def initialize(self) -> bool:
        """Initialize sensor connection"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=2,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            
            # Send wakeup command
            self.serial.write(b"WAKE\r\n")
            response = self.serial.readline()
            
            if b"READY" in response:
                self.logger.info(f"Sensor initialized on {self.port}")
                return True
            else:
                raise ConnectionError(f"Unexpected response: {response}")
                
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    async def read(self) -> Dict[str, Any]:
        """Read sensor data asynchronously"""
        try:
            # Request measurement
            self.serial.write(b"MEASURE\r\n")
            await asyncio.sleep(1)  # Wait for measurement
            
            # Read response
            response = self.serial.readline().decode().strip()
            
            # Parse CSV format: "8.14,25.3,35.2"
            values = response.split(',')
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "sensor_id": self.sensor_id,
                "parameters": {
                    "ph": float(values[0]),
                    "temperature": float(values[1]),
                    "salinity": float(values[2])
                },
                "units": self.unit_map,
                "quality_flag": "good"
            }
            
        except Exception as e:
            self.logger.error(f"Read failed: {e}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "sensor_id": self.sensor_id,
                "error": str(e),
                "quality_flag": "error"
            }
    
    def calibrate(self, calibration_data: Dict) -> bool:
        """Calibrate sensor"""
        try:
            # Send calibration commands
            if "ph_standard" in calibration_data:
                cmd = f"CAL_PH {calibration_data['ph_standard']}\r\n"
                self.serial.write(cmd.encode())
                response = self.serial.readline()
                
                if b"OK" in response:
                    self.logger.info("pH calibration successful")
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.error(f"Calibration failed: {e}")
            return False
```

Sensor Testing

```python
# tests/sensors/test_new_sensor.py
import pytest
import asyncio
from coralcore.sensors.new_sensor import NewSensor

@pytest.fixture
def mock_sensor():
    """Create mock sensor for testing"""
    sensor = NewSensor(port="/dev/ttyUSB99")  # Mock port
    sensor.serial = pytest.Mock()
    return sensor

@pytest.mark.asyncio
async def test_sensor_read(mock_sensor):
    """Test sensor read operation"""
    # Mock serial response
    mock_sensor.serial.readline.return_value = b"8.14,25.3,35.2\r\n"
    
    # Read data
    data = await mock_sensor.read()
    
    # Verify
    assert data["parameters"]["ph"] == 8.14
    assert data["parameters"]["temperature"] == 25.3
    assert data["parameters"]["salinity"] == 35.2
    assert data["quality_flag"] == "good"

def test_sensor_initialization(mock_sensor):
    """Test sensor initialization"""
    mock_sensor.serial.readline.return_value = b"READY\r\n"
    
    result = mock_sensor.initialize()
    
    assert result == True
    mock_sensor.serial.write.assert_called_with(b"WAKE\r\n")
```

---

📚 Contributing to Documentation

Documentation Structure

```
docs/
├── api/                    # API documentation
│   ├── physics.md
│   ├── sensors.md
│   └── analysis.md
├── tutorials/              # Step-by-step tutorials
│   ├── getting-started.md
│   ├── field-deployment.md
│   └── data-analysis.md
├── explanations/           # Conceptual guides
│   ├── rhi-explained.md
│   ├── acoustic-theory.md
│   └── calcification.md
├── references/             # Technical references
│   ├── parameters.md
│   ├── equations.md
│   └── sensors-specs.md
└── contributing/           # Contribution guides
    └── style-guide.md
```

Docstring Style

We use NumPy/Google style docstrings:

```python
def calculate_rhi(parameters: Dict[str, float], weights: Optional[Dict] = None) -> float:
    """
    Calculate Reef Health Index from eight parameters.
    
    The RHI is a weighted composite of normalized parameter values,
    ranging from 0 (critical degradation) to 1 (optimal health).
    
    Parameters
    ----------
    parameters : Dict[str, float]
        Dictionary containing the eight CORAL-CORE parameters:
        - g_ca : Calcification rate (mmol/cm²/day)
        - e_diss : Wave dissipation coefficient (0-1)
        - phi_ps : Quantum yield (0-0.8)
        - rho_skel : Skeletal density (g/cm³)
        - delta_ph : Acidification lag (pH units)
        - s_reef : Acoustic signature (entropy)
        - k_s : Roughness index (m)
        - t_thr : Bleaching threshold (°C)
    
    weights : Optional[Dict]
        Custom weights for each parameter. If None, uses PCA-derived
        weights from the 22-year reference dataset.
    
    Returns
    -------
    float
        Reef Health Index (0-1)
    
    Examples
    --------
    >>> params = {
    ...     'g_ca': 1.84, 'e_diss': 0.91, 'phi_ps': 0.67,
    ...     'rho_skel': 1.62, 'delta_ph': 0.08, 's_reef': 4.3,
    ...     'k_s': 0.15, 't_thr': 31.2
    ... }
    >>> rhi = calculate_rhi(params)
    >>> print(f"{rhi:.2f}")
    0.84
    
    Notes
    -----
    Reference thresholds:
    - RHI ≥ 0.80: Healthy reef
    - 0.50 ≤ RHI < 0.80: Moderate stress
    - RHI < 0.50: Critical degradation
    
    References
    ----------
    .. [1] Baladi, S. (2026). CORAL-CORE Research Paper.
           DOI: 10.5281/zenodo.18913829
    """
    pass
```

Building Documentation Locally

```bash
# Install documentation tools
pip install mkdocs mkdocs-material mkdocstrings

# Build docs
mkdocs build

# Serve locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

🧪 Testing Guidelines

Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── physics/
│   │   ├── test_calcification.py
│   │   ├── test_wave_dissipation.py
│   │   └── test_rhi.py
│   └── sensors/
│       ├── test_sami.py
│       └── test_amar.py
├── integration/            # Integration tests
│   ├── test_data_pipeline.py
│   └── test_sensor_fusion.py
├── field/                  # Field data validation
│   └── test_against_field_data.py
└── conftest.py             # Shared fixtures
```

Writing Tests

```python
# tests/unit/physics/test_calcification.py
import pytest
import numpy as np
from coralcore.physics.calcification import (
    calculate_calcification_rate,
    validate_against_field_data
)

class TestCalcification:
    """Test suite for calcification rate calculations"""
    
    @pytest.mark.parametrize("omega_a,phi_ps,temperature,species,expected", [
        (3.4, 0.65, 28.0, 'acropora', 2.14),  # Optimal conditions
        (2.5, 0.65, 28.0, 'acropora', 1.23),  # Lower saturation
        (3.4, 0.40, 28.0, 'acropora', 1.32),  # Stressed symbiosis
        (3.4, 0.65, 32.0, 'acropora', 0.0),    # Above bleaching threshold
    ])
    def test_calcification_values(self, omega_a, phi_ps, temperature, 
                                   species, expected):
        """Test calcification rate calculation"""
        result = calculate_calcification_rate(
            omega_a=omega_a,
            phi_ps=phi_ps,
            temperature=temperature,
            species=species
        )
        
        assert np.isclose(result, expected, rtol=0.1)
    
    def test_invalid_species(self):
        """Test error handling for invalid species"""
        with pytest.raises(KeyError):
            calculate_calcification_rate(
                omega_a=3.4,
                phi_ps=0.65,
                temperature=28.0,
                species="invalid_species"
            )
    
    def test_validation_against_field_data(self):
        """Test model validation with field data"""
        # Load field data
        field_data = load_field_data("ras_mohammed_2024")
        
        # Calculate predictions
        predictions = []
        observations = []
        
        for sample in field_data:
            pred = calculate_calcification_rate(
                omega_a=sample['omega_a'],
                phi_ps=sample['phi_ps'],
                temperature=sample['temperature'],
                species=sample['species']
            )
            predictions.append(pred)
            observations.append(sample['g_ca'])
        
        # Calculate metrics
        r2 = np.corrcoef(predictions, observations)[0, 1]**2
        
        # Should match paper's reported accuracy
        assert r2 > 0.85
```

Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=coralcore --cov-report=html

# Run specific test file
pytest tests/unit/physics/test_calcification.py -v

# Run tests matching pattern
pytest -k "calcification"

# Run with parallel execution
pytest -n auto

# Run slow tests only
pytest -m slow
```

---

🔀 Pull Request Process

PR Checklist

· Code follows project style guide
· Tests added/updated and passing
· Documentation updated
· CHANGELOG.md updated
· Benchmarks added if performance-critical
· All CI checks passing
· Reviewed by at least one maintainer

PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactor

## Related Issues
Closes #XXX

## Physics Changes
- [ ] Equations modified
- [ ] Constants updated
- [ ] Validation against field data
- [ ] Documentation updated

## Sensor Changes
- [ ] New sensor support
- [ ] Driver modifications
- [ ] Tested with hardware
- [ ] Documentation updated

## Testing Performed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Field data validation
- [ ] Performance benchmarks

## Additional Notes
Any additional information reviewers should know
```

Review Process

1. Automated Checks: CI runs tests, linting, type checking
2. Code Review: At least one maintainer reviews
3. Physics Review: If modifying core equations
4. Documentation Review: For documentation changes
5. Field Validation: For sensor/field-related changes

---

🌍 Community Guidelines

Communication Channels

· GitHub Issues: Bug reports, feature requests
· GitHub Discussions: Q&A, ideas, community support
· Email: gitdeeper@gmail.com (project lead)
· ORCID: 0009-0003-8903-0029

Recognition

Contributors are recognized in:

· AUTHORS.md
· Release notes
· Academic publications (where applicable)

Research Contributions

If you use CORAL-CORE in your research:

1. Cite the paper: Baladi, S. (2026). CORAL-CORE. DOI: 10.5281/zenodo.18913829
2. Share your data/code when possible
3. Submit a case study to our repository

Code of Conduct Enforcement

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned with this Code of Conduct.

---

📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CORAL-CORE! 🪸

For questions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
