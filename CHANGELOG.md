# Changelog

All notable changes to the CORAL-CORE project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**DOI:** 10.5281/zenodo.18913829  
**Repository:** github.com/gitdeeper8/coralcore

---

## [1.0.0] - 2026-03-08

### 🚀 Initial Release
- Publication of CORAL-CORE research paper in Coral Reefs (Springer)
- Release of complete 8-parameter physics framework
- Open access data from 14 reef systems (2003-2025)
- Interactive web dashboard at coralcore.netlify.app

### Added
#### Core Physics Engine
- Calcification rate calculator with power-law kinetics (n = 1.67 ± 0.12)
- Wave energy dissipation model with roughness coupling (E_diss up to 97%)
- Zooxanthellae quantum yield monitoring (Φ_ps 0.60-0.72 healthy range)
- Skeletal density analysis with open-cell foam mechanics
- Ocean acidification lag parameter (ΔpH early warning system)
- Acoustic signature processing with 96 kHz sampling
- Surface roughness index from photogrammetry
- Adaptive thermal bleaching threshold (T_thr dynamic model)

#### Reef Health Index (RHI)
- Composite index with PCA-derived weights
- 91.4% accuracy in bleaching prediction
- 32-day mean lead time before visible onset
- Real-time monitoring dashboard

#### Sensor Integration
- SAMI-alk pH/alkalinity sensor driver
- AMAR G4 acoustic recorder interface
- Diving-PAM fluorometer support
- ADCP Workhorse current profiler
- SBE37 MicroCAT CTD integration
- GoPro stereo photogrammetry pipeline

#### Deployment Options
- Single station deployment scripts
- Multi-station network architecture
- Cloud deployment (AWS/Azure/GCP)
- Edge computing for Raspberry Pi
- Docker containers for all services
- Netlify web dashboard

#### Documentation
- Complete API reference
- Field deployment guide
- Sensor calibration protocols
- Data analysis tutorials
- Contribution guidelines
- Code of conduct

### Changed
N/A - Initial release

### Deprecated
N/A - Initial release

### Removed
N/A - Initial release

### Fixed
N/A - Initial release

### Security
- JWT authentication for API endpoints
- Encrypted sensor data transmission
- Role-based access control
- Secure configuration management

---

## [0.9.0] - 2026-02-15

### ⚠️ Pre-release Candidate

### Added
- Beta version of all core modules
- Validation against 10 reef systems
- Preliminary RHI weight determination
- Basic sensor drivers
- Initial documentation

### Changed
- Refined calcification kinetics based on field data
- Updated acoustic processing algorithms
- Improved thermal threshold model

### Fixed
- SAMI-alk timeout issues
- ADCP data parsing errors
- Photogrammetry alignment problems

---

## [0.8.0] - 2026-01-20

### 🧪 Alpha Release

### Added
- Prototype physics modules
- Test deployments at Ras Mohammed
- Basic data collection pipeline
- Preliminary RHI formulation

---

## [0.1.0] - 2025-06-01

### 🎯 Project Initiation

### Added
- Project concept and framework design
- Initial parameter selection
- Literature review compilation
- Research proposal development

---

## 🔮 Future Releases

### [1.1.0] - Planned Q2 2026
- eDNA integration as 9th parameter
- Machine learning emulators
- Downscaled ocean chemistry projections
- Additional reef sites (Pacific, Indian Ocean)

### [1.2.0] - Planned Q4 2026
- Real-time satellite data integration
- Automated intervention recommendations
- Mobile app for field data collection
- Community science portal

### [2.0.0] - Planned 2027
- Global reef monitoring network
- AI-powered predictive modeling
- Bio-inspired engineering design tools
- Carbon credit integration

---

## 📊 Version History

| Version | Date | Status | DOI |
|---------|------|--------|-----|
| 1.0.0 | 2026-03-08 | Stable Release | 10.5281/zenodo.18913829 |
| 0.9.0 | 2026-02-15 | Release Candidate | 10.5281/zenodo.18813829 |
| 0.8.0 | 2026-01-20 | Alpha | 10.5281/zenodo.18713829 |
| 0.1.0 | 2025-06-01 | Concept | - |

---

## 📝 How to Update This Changelog

When contributing to CORAL-CORE, please add your changes to the "Unreleased" section:

```markdown
## [Unreleased]

### Added
- New feature X

### Changed
- Modified Y to improve Z

### Fixed
- Bug in component W
```

---

For questions or contributions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0022
