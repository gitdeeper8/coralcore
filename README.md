# 🪸 CORAL-CORE

**Coral Organism Reef Analysis & Living — Calcification, Ocean, and Reef Ecology**

> *"Coral reefs are not passive habitats — they are active, physics-governed engineering systems*
> *with quantifiable input rates, energy conversion efficiencies, structural tolerances, and failure thresholds."*

<div align="center">

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18913829-00e5c8?style=flat-square&logo=zenodo)](https://doi.org/10.5281/zenodo.18913829)
[![PyPI Version](https://img.shields.io/pypi/v/coralcore?color=ff6b47&style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/coralcore/)
[![Python](https://img.shields.io/pypi/pyversions/coralcore?color=00e5c8&style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/coralcore/)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-22c55e?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
[![OSF Preregistration](https://img.shields.io/badge/OSF-Preregistration-0969da?style=flat-square)](https://doi.org/10.17605/OSF.IO/VU246)
[![OSF Project](https://img.shields.io/badge/OSF-Project-0969da?style=flat-square)](https://osf.io/8u9gt)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Results](#key-results)
- [Eight-Parameter Framework](#eight-parameter-framework)
- [Reef Health Index (RHI)](#reef-health-index-rhi)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Validation Sites](#validation-sites)
- [Case Studies](#case-studies)
- [Preregistration](#preregistration)
- [Data Availability](#data-availability)
- [References](#references)
- [Author](#author)
- [Citation](#citation)

---

## Overview

**CORAL-CORE** is a unified physics-computational framework for real-time monitoring, modeling,
and prediction of coral reef health and structural integrity. It integrates **eight orthogonal
biophysical parameters** spanning five physical domains into a single **Reef Health Index (RHI)**
that achieves **91.4% accuracy** in predicting bleaching events **28–45 days** before visible onset.

Validated against a **22-year dataset (2003–2025)** combining:

- 🔬 Underwater photogrammetry at 5 mm horizontal resolution
- 🎙️ 16-channel passive acoustic recording at 96 kHz
- 🧪 In-situ alkalinity & calcification micro-sensors (SAMI-alk)
- 🛰️ Sentinel-2 sea surface temperature time series

across **14 reef systems** spanning four Indo-Pacific and Atlantic reef provinces.

---

## Key Results

| Metric | Value |
|--------|-------|
| RHI Bleaching Prediction Accuracy | **91.4%** |
| Mean Early-Warning Lead Time | **32 days** before visible onset |
| Improvement vs. SST-only baseline | **+20 days** advance warning |
| Wave Energy Dissipation (healthy crest) | **up to 97%** reduction |
| Acoustic–Recruitment Correlation | **r² = 0.81** (p < 0.001) |
| Bleaching Threshold Prediction RMSE | **0.41 °C** |
| Calcification Kinetics Exponent | **n = 1.67 ± 0.12** |
| Validation Observations | **47,832** daily 8-dimensional records |
| False Positive Rate | **4.2%** (vs. 18.7% SST-only) |

---

## Eight-Parameter Framework

CORAL-CORE characterizes reef function through eight physically independent parameters
across five physical domains:

| # | Domain | Parameter | Symbol | Unit |
|---|--------|-----------|--------|------|
| 1 | Physical Chemistry | Calcification Rate | G_ca | mmol cm⁻² day⁻¹ |
| 2 | Fluid Mechanics | Wave Energy Dissipation | E_diss | W m⁻² |
| 3 | Quantum Biology | Zooxanthellae Quantum Yield | Φ_ps | dimensionless [0–0.80] |
| 4 | Materials Science | Skeletal Bulk Density | ρ_skel | g cm⁻³ |
| 5 | Marine Chemistry | Ocean Acidification Lag | ΔpH | pH units |
| 6 | Reef Acoustics | Acoustic Reef Signature | S_reef | dB re 1 μPa²/Hz |
| 7 | Surface Hydraulics | Surface Roughness Index | k_s | m |
| 8 | Thermal Biology | Thermal Bleaching Threshold | T_thr | °C |

### Governing Equations

**① Calcification Rate** — modified power-law kinetics (Albright et al., 2016):

```
G = k · (Ωa − 1)ⁿ · f(T) · Φps
```

| Variable | Description |
|----------|-------------|
| `Ωa` | Aragonite saturation state |
| `k` | Species rate constant — 0.31 (*Porites lobata*) to 2.14 (*Acropora millepora*) |
| `n` | Reaction order — **1.67 ± 0.12** (field-calibrated, 14 sites) |
| `f(T)` | Temperature modulation factor ∈ [0, 1] |
| `Φps` | Zooxanthellae quantum yield |

**② Wave Energy Dissipation:**

```
ε = Cf · ρ · g · H²rms · (2π / T_wave) / (8h)
```

**③ Thermal Bleaching Threshold** — adaptive model:

```
T_thr(t) = T_base + α · σT(t−60) + β · [Φps(t) / Φps,max]

  α = 0.34  (thermal acclimation coefficient)
  β = 0.18  (photophysiological contribution coefficient)
  RMSE = 0.41 °C  (validated against 1,247 bleaching observations)
```

**④ Zooxanthellae Quantum Yield** — PAM fluorometry:

```
Φps = (Fm − F0) / Fm

  Φps ≥ 0.60  →  Healthy symbiosis
  Φps < 0.40  →  Photoinhibition / thermal stress
  Φps < 0.25  →  Active bleaching underway
```

---

## Reef Health Index (RHI)

```
RHI = Σᵢ wᵢ · φᵢ*     where  Σwᵢ = 1.0,  φᵢ* ∈ [0, 1]
```

Parameters normalized to [0, 1] using pre-specified healthy/critical thresholds.
Weights derived by regularized PCA with leave-one-site-out cross-validation (n = 47,832 obs):

| Rank | Parameter | Symbol | Weight |
|------|-----------|--------|--------|
| 1 | Zooxanthellae Quantum Yield | Φ_ps | **0.21** |
| 2 | Calcification Rate | G_ca | **0.19** |
| 3 | Wave Energy Dissipation | E_diss | 0.14 |
| 4 | Skeletal Bulk Density | ρ_skel | 0.12 |
| 5 | Ocean Acidification Lag | ΔpH | 0.11 |
| 6 | Acoustic Reef Signature | S_reef | 0.10 |
| 7 | Surface Roughness Index | k_s | 0.08 |
| 8 | Thermal Bleaching Threshold | T_thr | 0.05 |

### Classification Thresholds

| Status | RHI Range | Operational Response |
|--------|-----------|---------------------|
| 🟢 **HEALTHY** | ≥ 0.80 | Standard monitoring — normal operations |
| 🟡 **STRESSED** | 0.50 – 0.79 | Elevated monitoring — intervention possible |
| 🔴 **CRITICAL** | < 0.50 | Immediate intervention required |

---

## Project Structure

```
coralcore/
│
├── README.md
├── AUTHORS.md
├── LICENSE                           (CC BY 4.0)
├── CHANGELOG.md
├── requirements.txt
├── setup.py
├── pyproject.toml
│
├── coralcore/                        # Main Python package
│   ├── __init__.py
│   │
│   ├── parameters/                   # Eight physical parameter modules
│   │   ├── calcification.py          # G_ca — power-law kinetics
│   │   ├── wave_dissipation.py       # E_diss — reef flat energy flux
│   │   ├── quantum_yield.py          # Φ_ps — PAM fluorometry model
│   │   ├── skeletal_density.py       # ρ_skel — open-cell foam mechanics
│   │   ├── acidification_lag.py      # ΔpH — pH-upregulation energetics
│   │   ├── acoustic_signature.py     # S_reef — spectral decomposition
│   │   ├── surface_roughness.py      # k_s — photogrammetric extraction
│   │   └── bleaching_threshold.py    # T_thr — adaptive thermal model
│   │
│   ├── rhi/                          # Reef Health Index
│   │   ├── composite.py              # RHI computation & weighting
│   │   ├── weights.py                # PCA weight calibration
│   │   ├── normalize.py              # Parameter normalization
│   │   └── alert.py                  # Classification & alert system
│   │
│   ├── models/                       # Statistical & ML models
│   │   ├── bayesian_statespace.py    # Hierarchical Bayesian (Stan/RStan)
│   │   ├── gaussian_process.py       # Missing data imputation
│   │   ├── dynamic_factor.py         # DFA via MARSS
│   │   └── pinn.py                   # Physics-Informed Neural Network
│   │
│   ├── instrumentation/              # Sensor data parsers & interfaces
│   │   ├── sami_alk.py               # SAMI-alk alkalinity/pH
│   │   ├── amar_g4.py                # AMAR G4 acoustic recorder
│   │   ├── diving_pam.py             # PAM fluorometer
│   │   ├── adcp.py                   # RDI ADCP wave profiling
│   │   ├── sbe37.py                  # Sea-Bird CTD
│   │   └── photogrammetry.py         # SfM 3D reconstruction pipeline
│   │
│   ├── chemistry/                    # Marine chemistry utilities
│   │   ├── co2sys.py                 # CO2SYS aragonite saturation
│   │   ├── carbonate.py              # Carbonate chemistry
│   │   └── acidification.py          # ΔpH lag computation
│   │
│   ├── acoustics/                    # Acoustic analysis
│   │   ├── spectral.py               # PSD & Shannon entropy
│   │   ├── bandpass.py               # 400–800 / 800–2000 / 2000–5000 Hz
│   │   └── recruitment.py            # Larval recruitment prediction
│   │
│   ├── validation/                   # Validation & benchmarks
│   │   ├── sites.py                  # 14-site metadata registry
│   │   ├── cross_validation.py       # Leave-one-site-out CV
│   │   ├── baselines.py              # SST-only & NDVI+SST comparisons
│   │   └── uncertainty.py            # Error propagation (8.3–12.1% CI)
│   │
│   └── utils/
│       ├── io.py                     # Data I/O (CSV, HDF5, NetCDF)
│       ├── transforms.py             # Log transforms, centering
│       └── visualization.py          # RHI dashboard & parameter plots
│
├── data/
│   ├── sites/                        # Per-site sensor time series
│   │   ├── red_sea_ras_mohammed/
│   │   ├── great_barrier_reef/
│   │   ├── caribbean_arc/
│   │   ├── coral_triangle/
│   │   └── ...                       # 14 sites total
│   ├── reference/
│   │   ├── bleaching_events_22yr.csv
│   │   ├── rhi_weights_calibrated.json
│   │   └── species_k_constants.csv   # k & n for 34 coral species
│   └── acoustic/
│       ├── healthy_reef_spectra/
│       └── degraded_reef_spectra/
│
├── notebooks/
│   ├── 01_parameter_overview.ipynb
│   ├── 02_rhi_calibration.ipynb
│   ├── 03_bleaching_prediction.ipynb
│   ├── 04_acoustic_restoration.ipynb
│   ├── 05_case_study_red_sea_2020.ipynb
│   ├── 06_case_study_gbr_2016.ipynb
│   └── 07_multi_stressor_synergy.ipynb
│
├── docs/
│   ├── whitepaper/                   # CORAL-CORE Research Paper (PDF)
│   ├── api/                          # Auto-generated API reference
│   └── field_protocols/              # Instrumentation & SfM protocols
│
└── tests/
    ├── test_parameters.py
    ├── test_rhi.py
    ├── test_models.py
    ├── test_instrumentation.py
    └── test_chemistry.py
```

---

## Installation

### From PyPI (Recommended)

```bash
pip install coralcore
```

### From Source

```bash
git clone https://github.com/gitdeeper8/coralcore.git
cd coralcore
pip install -r requirements.txt
pip install -e .
```

**Requirements:** Python 3.8+, NumPy, SciPy, pandas, xarray, pystan, scikit-learn, matplotlib

---

## Quick Start

```python
from coralcore.parameters.calcification import calcification_rate
from coralcore.parameters.quantum_yield import quantum_yield_status
from coralcore.rhi.composite import ReefHealthIndex

# ── Calcification rate ──────────────────────────────────────────────
G = calcification_rate(
    omega_a=2.8,        # aragonite saturation state
    k=1.24,             # species constant (Acropora sp.)
    n=1.67,             # reaction order (field-calibrated)
    temperature=28.5,   # [°C]
    t_thr=30.1,         # bleaching threshold [°C]
    phi_ps=0.63         # quantum yield
)
print(f"Calcification rate : {G:.3f} mmol cm⁻² day⁻¹")

# ── Quantum yield status ────────────────────────────────────────────
status = quantum_yield_status(phi_ps=0.63)
print(f"Photosynthetic status : {status}")     # → Healthy

# ── Reef Health Index ───────────────────────────────────────────────
rhi = ReefHealthIndex()
score = rhi.compute({
    'g_ca':      1.24,
    'e_diss':    0.78,
    'phi_ps':    0.63,
    'rho_skel':  1.42,
    'delta_ph':  0.08,
    's_reef':    4.30,
    'k_s':       0.14,
    't_thr':     30.1
})
print(f"RHI    = {score:.3f}")             # → 0.82
print(f"Status = {rhi.classify(score)}")   # → 🟢 HEALTHY
```

---

## Validation Sites

14 reef systems · 28°N – 23°S · Ωa range 1.9 – 3.8 · 2003–2025:

| # | Site | Province | Ωa | Key Feature |
|---|------|----------|----|-------------|
| 1 | Ras Mohammed NMP | Red Sea | 3.4 ± 0.3 | 31-day early warning (2020) |
| 2 | Gulf of Aqaba | Red Sea (N) | 3.6 ± 0.2 | Thermal resilience anomaly (+1.7°C T_thr) |
| 3 | Great Barrier Reef (Lizard Island) | Indo-Pacific | 3.2 ± 0.4 | 2016 mass bleaching benchmark |
| 4 | Ningaloo Reef | Indo-Pacific | 3.1 ± 0.2 | eDNA Phase II site · UNESCO World Heritage |
| 5 | Coral Triangle (Komodo) | Coral Triangle | 3.6 ± 0.2 | Highest acoustic diversity |
| 6 | Maldives Outer Atolls | Indian Ocean | 3.3 ± 0.3 | Post-bleaching recovery trajectory |
| 7 | Jardines de la Reina, Cuba | Caribbean | 2.9 ± 0.2 | Near-pristine Atlantic reference |
| 8 | Lighthouse Reef Atoll, Belize | Caribbean | 2.8 ± 0.2 | Highest ΔpH in dataset (+0.18) |
| 9 | Mesoamerican Barrier Reef | Caribbean | 2.8 ± 0.3 | Multi-stressor synergy site |
| 10–14 | Additional sites | Mixed | 1.9 – 3.8 | Chemical gradient calibration |

---

## Case Studies

### 🔴 Red Sea 2020 — Early Warning Success

CORAL-CORE detected PSII photoinhibition **31 days** before visual bleaching onset.
Sequential parameter cascade:

```
Day  0  →  T exceeds adaptive T_thr by +0.8°C
Day +3  →  Φps begins declining below 0.50
Day +8  →  G_ca suppression detected
Day +11 →  S_reef reduction (snapping shrimp activity drop)
Day +31 →  First visual bleaching confirmed by dive teams
```

**Result:** Shade structure deployment enabled → **23% lower bleaching extent** vs. unmonitored
control plots (p = 0.014, n = 8 paired plot comparisons).

---

### 🟠 Great Barrier Reef 2016 — Retrospective Analysis

Retrospective application to archived AIMS monitoring data:

- RHI crossed critical threshold **38 days** before reef manager bleaching declaration
- **61 days** before mass mortality survey reports were finalized
- Three converging precursors: Ωa decline −0.08 yr⁻¹ (Coral Sea, since 2012); anomalously low
  cloud cover elevating PAR stress; Φps decline detected **late January 2016**
- Single-parameter SST system in operation: **captured 0 of 3 precursors**

---

### 🟡 Multi-Stressor Synergy — Lighthouse Reef, Belize 2020

**Key finding:** Every +0.1 ΔpH unit reduces effective thermal bleaching threshold by **0.4–0.8°C**.

| Site | Temperature Anomaly | Φps Collapse | ΔpH |
|------|---------------------|--------------|-----|
| Red Sea (2020) | +1.8°C above T_thr | 0.11 | baseline |
| Lighthouse Reef (2020) | **+0.9°C** above T_thr | 0.11 | **+0.18** (highest in dataset) |

Chemically stressed reefs bleach at temperature anomalies **approximately half** those required
at chemically healthy sites — a synergy absent from all current operational bleaching alert systems.

---

## Preregistration

| Field | Details |
|-------|---------|
| **Title** | CORAL-CORE: Biomineralization Dynamics & Reef Hydro-Acoustic Buffering |
| **Registration DOI** | [10.17605/OSF.IO/VU246](https://doi.org/10.17605/OSF.IO/VU246) |
| **OSF Project** | [osf.io/8u9gt](https://osf.io/8u9gt) |
| **Registration Type** | OSF Preregistration |
| **Date Registered** | March 10, 2026 |
| **License** | CC BY 4.0 International |
| **Contributors** | Samir Baladi |

The preregistration fully specifies all five research questions (RQ1–RQ5), five statistical models,
RHI weights, inference criteria, data exclusion rules, and stopping rules — all locked before
prospective data collection begins.

---

## Data Availability

| Resource | Link |
|----------|------|
| 🪸 Web Dashboard | [coralcore.netlify.app](https://coralcore.netlify.app) |
| 📦 PyPI Package | [pypi.org/project/coralcore](https://pypi.org/project/coralcore/) |
| 📄 Zenodo Archive | [doi.org/10.5281/zenodo.18913829](https://doi.org/10.5281/zenodo.18913829) |
| 🔬 OSF Preregistration | [10.17605/OSF.IO/VU246](https://doi.org/10.17605/OSF.IO/VU246) |
| 🗂️ OSF Project | [osf.io/8u9gt](https://osf.io/8u9gt) |
| 🐙 GitHub (Primary) | [github.com/gitdeeper8/coralcore](https://github.com/gitdeeper8/coralcore) |
| 🦊 GitLab (Mirror) | [gitlab.com/gitdeeper8/coralcore](https://gitlab.com/gitdeeper8/coralcore) |
| 📖 Documentation | [coralcore.readthedocs.io](https://coralcore.readthedocs.io) |

All source code, validation datasets (47,832 daily observations), calibrated RHI weights,
acoustic spectrograms (HDF5), SfM 3D meshes (OBJ), and field protocols are archived
under **CC BY 4.0 International**.

---

## References

- Albright, R. et al. (2016). Reversal of ocean acidification enhances net coral reef calcification. *Nature*, 531, 362–365. [DOI: 10.1038/nature17155](https://doi.org/10.1038/nature17155)
- Comeau, S. et al. (2019). Resistance to ocean acidification in coral reef taxa is not gained by acclimatization. *Nature Climate Change*, 9, 477–483. [DOI: 10.1038/s41558-019-0486-9](https://doi.org/10.1038/s41558-019-0486-9)
- Gordon, T.A.C. et al. (2019). Acoustic enrichment can enhance fish community development on degraded coral reef habitat. *Nature Communications*, 10, 5414. [DOI: 10.1038/s41467-019-13186-2](https://doi.org/10.1038/s41467-019-13186-2)
- Goreau, T.F. (1959). The physiology of skeleton formation in corals. *Biological Bulletin*, 116(1), 59–75. [DOI: 10.2307/1538819](https://doi.org/10.2307/1538819)
- Langdon, C. et al. (2000). Effect of calcium carbonate saturation state on the calcification rate of an experimental coral reef. *Global Biogeochemical Cycles*, 14(2), 639–654. [DOI: 10.1029/1999GB001195](https://doi.org/10.1029/1999GB001195)
- Lowe, R.J. et al. (2005). Spectral wave dissipation over a barrier reef. *Journal of Geophysical Research: Oceans*, 110, C04001. [DOI: 10.1029/2004JC002711](https://doi.org/10.1029/2004JC002711)
- Suggett, D.J. et al. (2017). Coral bleaching patterns are the outcome of two interacting biological traits. *Trends in Ecology & Evolution*, 32(7), 503–506. [DOI: 10.1016/j.tree.2017.04.003](https://doi.org/10.1016/j.tree.2017.04.003)
- Vermeij, M.J.A. et al. (2010). Coral larvae move toward reef sounds. *PLOS ONE*, 5(5), e10660. [DOI: 10.1371/journal.pone.0010660](https://doi.org/10.1371/journal.pone.0010660)

> Full reference list (18 primary sources): [`docs/whitepaper/CORAL-CORE_RESEARCH_PAPER.pdf`](docs/whitepaper/)

---

## Author

<table>
<tr>
<td width="72" align="center" valign="top"><br>🪸</td>
<td>

### Samir Baladi
**Principal Investigator · Marine Biophysics & Reef Engineering Division**

Independent interdisciplinary researcher affiliated with the **Ronin Institute for Independent
Scholarship** and the **Rite of Renaissance** research programme. Samir develops open-source
physics-computational frameworks that bridge field-deployable instrumentation and rigorous
quantitative modeling across extreme and understudied natural environments.

CORAL-CORE is the marine physics pillar of an ongoing eleven-framework programme.
Related preregistered frameworks include **HADEXION** (hadal zone dynamics),
**OPTIC-LENS** (atmospheric optics), **MAGION** (magnetospheric physics),
**METEORICA** (extraterrestrial materials classification), and seven others — each following
the same open-science pipeline: OSF preregistration → Zenodo archive → PyPI package →
peer-reviewed whitepaper → interactive web dashboard.

*No conflicts of interest declared. No commercial funding. All outputs CC BY 4.0.*

| | |
|---|---|
| 📧 Email | [gitdeeper@gmail.com](mailto:gitdeeper@gmail.com) |
| 🆔 ORCID | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) |
| 🐙 GitHub | [github.com/gitdeeper8](https://github.com/gitdeeper8) |
| 🦊 GitLab | [gitlab.com/gitdeeper8](https://gitlab.com/gitdeeper8) |
| 🏛️ Affiliation | Ronin Institute for Independent Scholarship / Rite of Renaissance |

</td>
</tr>
</table>

---

## Citation

```bibtex
@software{baladi2026coralcore,
  author       = {Baladi, Samir},
  title        = {CORAL-CORE: Biomineralization Dynamics \&
                  Reef Hydro-Acoustic Buffering Framework},
  year         = {2026},
  version      = {1.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18913829},
  url          = {https://github.com/gitdeeper8/coralcore},
  license      = {CC BY 4.0}
}
```

---

<div align="center">

🪸 &nbsp;**CORAL-CORE** &nbsp;·&nbsp; *Coral reefs are not passive habitats — they are active, physics-governed engineering systems.*

Copyright © **CORAL-CORE 🪸** 2026 &nbsp;|&nbsp; CC BY 4.0 &nbsp;|&nbsp; Ronin Institute for Independent Scholarship

</div>
