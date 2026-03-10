# 🪸 CORAL-CORE Installation Guide v1.0.0

## Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework

**DOI**: 10.5281/zenodo.18913829  
**Repository**: github.com/gitdeeper8/coralcore  
**Web**: coralcore.netlify.app

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+, Debian 11+, macOS 12+, Windows 10/11 (WSL2)
- **RAM**: 8 GB
- **Storage**: 20 GB free space
- **Python**: 3.9 - 3.11
- **CUDA**: Optional (for GPU acceleration)

### Recommended Requirements
- **RAM**: 16+ GB
- **Storage**: 50+ GB SSD
- **GPU**: NVIDIA with 8+ GB VRAM (for 3D reconstruction)
- **Python**: 3.10
- **Docker**: 20.10+ (for containerized deployment)

### Sensor Data Requirements
- **SAMI-alk sensors**: USB 2.0+ interface
- **AMAR G4 acoustic recorders**: USB 3.0 or network storage
- **Diving-PAM fluorometer**: Serial/USB adapter
- **ADCP Workhorse**: Ethernet connection
- **SBE37 MicroCAT**: Serial/USB adapter
- **GoPro Hero12 stereo system**: WiFi or SD card transfer

---

## 🚀 Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/gitdeeper8/coralcore.git
cd coralcore
```

2. Create Virtual Environment

```bash
# Using venv (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda (alternative)
conda create -n coralcore python=3.10
conda activate coralcore
```

3. Install Dependencies

```bash
# Basic installation
pip install --upgrade pip
pip install -r requirements.txt

# Development installation (includes testing tools)
pip install -e .[dev]

# With GPU support for 3D reconstruction
pip install -e .[gpu]
```

4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

5. Run Initial Setup

```bash
# Initialize database and directories
python scripts/init_coralcore.py

# Download sample datasets
python scripts/download_samples.py

# Run system check
python scripts/verify_installation.py
```

---

🐳 Docker Installation

Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

Using Docker (Individual Containers)

```bash
# Build the image
docker build -t coralcore:latest .

# Run the container
docker run -d \
  --name coralcore \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/.env:/app/.env \
  coralcore:latest

# Development container with hot reload
docker run -d \
  --name coralcore-dev \
  -p 8000:8000 \
  -v $(pwd):/app \
  -v $(pwd)/data:/app/data \
  coralcore:dev
```

---

🔧 Detailed Installation by Component

Core Physics Engine

```bash
# Install numerical computing libraries
pip install numpy==1.24.3 scipy==1.10.1 numba==0.57.0

# Install physics simulation modules
pip install matplotlib==3.7.1 sympy==1.11.1
```

Data Processing Pipeline

```bash
# Install data processing tools
pip install pandas==2.0.0 xarray==2023.4.0 netCDF4==1.6.3
pip install h5py==3.8.0 tables==3.8.0
```

3D Photogrammetry

```bash
# Install photogrammetry dependencies
pip install opencv-python==4.7.0.72 open3d==0.17.0
pip install pycolmap==0.5.0 pyceres==2.2.0

# For Agisoft Metashape integration (optional)
pip install metashape==2.0.0
```

Acoustic Processing

```bash
# Install audio processing libraries
pip install librosa==0.10.0 soundfile==0.12.1
pip install pyhydrophone==0.1.3 pydal==0.3.0
```

Machine Learning & Analysis

```bash
# Install ML libraries
pip install scikit-learn==1.2.2 pytorch-lightning==2.0.0
pip install tensorflow==2.12.0 keras==2.12.0

# For Bayesian state-space modeling
pip install pystan==3.5.0 arviz==0.15.0
```

Visualization

```bash
# Install visualization tools
pip install plotly==5.14.1 dash==2.9.3
pip install seaborn==0.12.2 bokeh==3.1.0
```

---

📊 Sensor-Specific Setup

SAMI-alk pH/ALK Sensor

```bash
# Install SAMI communication drivers
pip install pyserial==3.5 pyusb==1.2.1

# Configure USB permissions
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666"' | sudo tee /etc/udev/rules.d/99-sami.rules
sudo udevadm control --reload-rules
```

AMAR G4 Acoustic Recorder

```bash
# Install acoustic processing tools
pip install obspy==1.4.0 echopype==0.6.0

# Mount AMAR storage (if network-attached)
mkdir -p /mnt/amar
sudo mount -t nfs 192.168.1.100:/data /mnt/amar -o nolock
```

Diving-PAM Fluorometer

```bash
# Install PAM communication tools
pip install pyvisa==1.13.0 pyvisa-py==0.5.3

# Configure serial port
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

---

🌐 Web Dashboard Deployment

Local Development Server

```bash
# Start the development server
python web/app.py

# Access at http://localhost:5000
```

Production Deployment (Gunicorn)

```bash
# Install production server
pip install gunicorn==20.1.0

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 web.app:app
```

Netlify Deployment

```bash
# Build static files
python web/build_static.py

# Deploy to Netlify (manual)
# 1. Push to GitHub repository
# 2. Connect repository to Netlify
# 3. Set build command: "python web/build_static.py"
# 4. Set publish directory: "web/build"

# Or use Netlify CLI
npm install -g netlify-cli
netlify deploy --prod --dir=web/build
```

---

🧪 Testing Installation

Run Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-xdist

# Run all tests
pytest tests/ -v --cov=coralcore

# Run specific test modules
pytest tests/test_physics.py -v
pytest tests/test_acoustic.py -v
pytest tests/test_photogrammetry.py -v
```

Verify Parameter Calculations

```bash
# Test calcification rate calculation
python scripts/test_calcification.py --site "Ras Mohammed" --date "2024-01-15"

# Test wave dissipation model
python scripts/test_wave_dissipation.py --hs 2.0 --tp 8.0

# Test acoustic signature analysis
python scripts/test_acoustic.py --file samples/reef_sound.wav
```

Validate RHI Computation

```bash
# Compute RHI for sample data
python scripts/compute_rhi.py --sample --verbose

# Expected output:
# RHI = 0.84 (Healthy reef)
# Components:
#   G_ca: 1.84 mmol/cm²/day
#   E_diss: 91%
#   Φ_ps: 0.67
#   ρ_skel: 1.62 g/cm³
#   ΔpH: 0.08 units
#   S_reef: 4.3 entropy
#   k_s: 0.15 m
#   T_thr: 31.2°C
```

---

❗ Troubleshooting

Common Issues and Solutions

Issue Solution
SAMI-alk not detected Check USB connection: lsusb \| grep FTDI Verify permissions: sudo chmod 666 /dev/ttyUSB*
PAM fluorometer timeout Check baud rate: 19200 Verify COM port: python -m serial.tools.list_ports
ADCP no data Check IP configuration: ping 192.168.1.100 Verify NTP sync: ntpq -p
CUDA out of memory Reduce batch size in config Use CPU fallback: export CUDA_VISIBLE_DEVICES=""
3D reconstruction fails Check OpenCV installation Verify image format: file samples/*.jpg

Log Files

```bash
# View application logs
tail -f logs/coralcore.log

# View sensor logs
tail -f logs/sensors/sami.log
tail -f logs/sensors/amar.log

# View error logs
tail -f logs/error.log
```

System Check

```bash
# Run comprehensive diagnostic
python scripts/diagnose.py --all

# Check sensor connections
python scripts/check_sensors.py --list

# Verify database integrity
python scripts/verify_db.py --repair
```

---

📚 Additional Resources

· Documentation: https://coralcore.netlify.app/docs
· API Reference: https://coralcore.netlify.app/api
· Tutorials: https://coralcore.netlify.app/tutorials
· GitHub Issues: https://github.com/gitdeeper8/coralcore/issues
· Discussion Forum: https://github.com/gitdeeper8/coralcore/discussions

---

📄 License

CORAL-CORE is released under the MIT License. See LICENSE file for details.

---

For support: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
DOI: 10.5281/zenodo.18913829 · Web: coralcore.netlify.app
