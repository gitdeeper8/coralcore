# 🪸 CORAL-CORE Deployment Guide (Detailed)
## Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework

**DOI**: 10.5281/zenodo.18913829  
**Repository**: github.com/gitdeeper8/coralcore  
**Web**: coralcore.netlify.app

---

## 📋 Table of Contents
- [Deployment Architectures](#deployment-architectures)
- [Single Station Deployment](#single-station-deployment)
- [Multi-Station Network](#multi-station-network)
- [Cloud Deployment](#cloud-deployment)
- [Edge Computing](#edge-computing)
- [Sensor Integration](#sensor-integration)
- [Data Pipeline](#data-pipeline)
- [Monitoring & Alerts](#monitoring--alerts)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

---

## 🏗️ Deployment Architectures

### Architecture Comparison

| Architecture | Use Case | Pros | Cons | Cost |
|-------------|----------|------|------|------|
| **Single Station** | Remote reef monitoring | Simple, low latency | Limited scalability | Low |
| **Multi-Station Network** | Regional reef systems | Scalable, redundant | Complex setup | Medium |
| **Cloud-Based** | Global monitoring | Highly scalable, accessible | Internet dependent | High |
| **Edge Computing** | Real-time alerts | Low latency, offline capable | Limited compute | Medium |

---

## 🖥️ Single Station Deployment

### Hardware Requirements
```yaml
Minimum Specifications:
  CPU: Intel NUC i5 / Raspberry Pi 4 (8GB)
  RAM: 8GB
  Storage: 1TB SSD
  Network: 4G/LTE modem
  Power: Solar + Battery backup (200W panel, 200Ah battery)
  Enclosure: IP67 waterproof case
  Sensors: SAMI-alk, AMAR G4, PAM, ADCP, SBE37, GoPro
```

Installation Steps

```bash
# 1. Prepare the system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip docker.io docker-compose

# 2. Clone repository
git clone https://github.com/gitdeeper8/coralcore.git
cd coralcore

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your station details

# 4. Install dependencies
pip install -r requirements.txt
pip install -e .

# 5. Test sensors
python scripts/test_sensors.py --all

# 6. Start services
docker-compose -f docker-compose.dev.yml up -d

# 7. Verify deployment
curl http://localhost:5000/health
```

Station Configuration Example

```yaml
# config/station_ras_mohammed.yaml
station:
  id: "RAS_MOHAMMED_01"
  name: "Ras Mohammed National Park"
  latitude: 27.75
  longitude: 34.23
  depth: 15
  province: "Indo-Pacific"
  deployment_date: "2026-03-08"

sensors:
  sami:
    port: "/dev/ttyUSB0"
    baudrate: 9600
    interval: 900
  amar:
    mount: "/mnt/amar"
    sample_rate: 96000
    gain: 0
  pam:
    port: "/dev/ttyUSB1"
    interval: 3600
  adcp:
    ip: "192.168.1.100"
    port: 5000
  sbe37:
    port: "/dev/ttyUSB2"
    interval: 60

data:
  storage: "/data/coralcore"
  retention_days: 365
  backup_interval: 86400

network:
  sync_interval: 3600
  cloud_endpoint: "https://api.coralcore.netlify.app"
  use_4g: true

power:
  source: "solar"
  panel_wattage: 200
  battery_ah: 200
  low_power_mode: true
```

---

🌐 Multi-Station Network

Network Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Station 1  │────▶│  Station 2  │────▶│  Station 3  │
│ Red Sea     │     │ Ningaloo    │     │ GBR         │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ▼
                    ┌─────────────┐
                    │   Cloud     │
                    │   Hub       │
                    └─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Database   │    │   Dashboard │    │   Alert     │
│  Cluster    │    │   Servers   │    │   System    │
└─────────────┘    └─────────────┘    └─────────────┘
```

Central Hub Configuration

```yaml
# config/hub_config.yaml
hub:
  id: "CORALCORE_HUB_01"
  region: "global"
  endpoints:
    api: "https://api.coralcore.netlify.app"
    websocket: "wss://ws.coralcore.netlify.app"
    mqtt: "mqtt.coralcore.netlify.app:8883"

database:
  primary:
    type: "timescaledb"
    host: "timescaledb.coralcore.net"
    port: 5432
    name: "coralcore_ts"
    user: "coraluser"
    pool_size: 100
  
  replica:
    - host: "replica1.coralcore.net"
    - host: "replica2.coralcore.net"

  cache:
    type: "redis"
    host: "redis.coralcore.net"
    port: 6379
    max_memory: "8gb"

message_queue:
  type: "rabbitmq"
  cluster: 
    - host: "rabbit1.coralcore.net"
    - host: "rabbit2.coralcore.net"
    - host: "rabbit3.coralcore.net"
  vhost: "coralcore"

stations:
  - id: "RAS_MOHAMMED_01"
    sync_interval: 300
    priority: 1
  - id: "NINGALOO_01"
    sync_interval: 600
    priority: 2
  - id: "GBR_LIZARD_01"
    sync_interval: 900
    priority: 3
```

---

☁️ Cloud Deployment

AWS Deployment (Terraform)

```hcl
# main.tf - AWS Infrastructure
provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "coralcore" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "coralcore-vpc"
    Project = "CORAL-CORE"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "coralcore" {
  name = "coralcore-cluster"
  
  setting {
    name = "containerInsights"
    value = "enabled"
  }
}

# RDS for TimescaleDB
resource "aws_db_instance" "timescaledb" {
  identifier = "coralcore-timescaledb"
  engine = "postgres"
  engine_version = "15.3"
  instance_class = "db.r5.2xlarge"
  allocated_storage = 1000
  storage_encrypted = true
  
  db_name = "coralcore"
  username = "coraladmin"
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
  
  backup_retention_period = 30
  backup_window = "03:00-04:00"
}
```

GCP Deployment

```bash
# Create GKE cluster
gcloud container clusters create coralcore-cluster \
  --num-nodes=3 \
  --machine-type=e2-standard-8 \
  --zone=us-central1-a \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=10

# Deploy with Helm
helm repo add coralcore https://coralcore.netlify.app/charts
helm install coralcore coralcore/coralcore \
  --set environment=production \
  --set database.type=CloudSQL \
  --set storage.type=GCS
```

Azure Deployment

```powershell
# Create AKS cluster
az aks create `
  --resource-group coralcore-rg `
  --name coralcore-aks `
  --node-count 3 `
  --node-vm-size Standard_D8s_v3 `
  --enable-addons monitoring `
  --enable-cluster-autoscaler `
  --min-count 3 `
  --max-count 10
```

---

📡 Edge Computing Deployment

Raspberry Pi Field Station

```bash
# setup_raspberry_pi.sh
#!/bin/bash

echo "🪸 Setting up CORAL-CORE Edge Station on Raspberry Pi"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git \
  libatlas-base-dev libhdf5-dev libopenblas-dev

# Enable interfaces
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker pi

# Clone repository
git clone https://github.com/gitdeeper8/coralcore.git
cd coralcore

# Create optimized config
cat > config/edge.yaml << 'YAML'
mode: "edge"
processing:
  batch_size: 100
  max_workers: 2
  use_gpu: false
  precision: "float16"
storage:
  local_path: "/mnt/data/coralcore"
  max_size_gb: 100
network:
  sync_interval: 3600
  compress_data: true
  use_4g: true
alerts:
  local: true
  cloud: true
  threshold_rhi: 0.5
YAML

# Install Python packages
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir tflite-runtime
```

---

🔌 Sensor Integration

USB Device Rules

```bash
# 99-sensors.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="sami", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="1bcF", ATTRS{idProduct}=="0005", SYMLINK+="amar", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="pam", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", SYMLINK+="sbe37", MODE="0666"
```

Sensor Testing

```bash
# Test all sensors
python scripts/test_sensors.py --all

# Test specific sensor
python scripts/test_sensor.py --type sami --port /dev/ttyUSB0
```

---

🔔 Monitoring & Alerts

Prometheus Configuration

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'coralcore-stations'
    static_configs:
      - targets:
        - 'ras-mohammed:9100'
        - 'ningaloo:9100'
        - 'gbr:9100'
```

Alert Rules

```yaml
# prometheus/alerts.yml
groups:
  - name: coralcore_alerts
    rules:
      - alert: BleachingImminent
        expr: coralcore_rhi < 0.5
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "Bleaching imminent at {{ $labels.station }}"
```

---

💾 Backup & Recovery

Automated Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/data/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="coralcore_backup_${DATE}.tar.gz"

# Backup PostgreSQL
pg_dump -U coraluser -h localhost coralcore > ${BACKUP_DIR}/database/coralcore_${DATE}.sql

# Backup configuration
tar -czf ${BACKUP_DIR}/config/config_${DATE}.tar.gz config/

# Create archive
tar -czf ${BACKUP_DIR}/${BACKUP_FILE} ${BACKUP_DIR}/*

# Upload to cloud
aws s3 cp ${BACKUP_DIR}/${BACKUP_FILE} s3://${AWS_S3_BUCKET}/backups/
```

---

🆘 Troubleshooting

Common Issues

Issue Solution
Sensor not detected Check USB: lsusb Check permissions: ls -la /dev/ttyUSB*
Database connection failed Verify credentials in .env Check logs: docker-compose logs postgres
Docker won't start Check logs: docker-compose logs Verify port availability
Cloud sync failing Check internet Verify API key Check endpoint URL

---

📚 References

· CORAL-CORE Research Paper: DOI: 10.5281/zenodo.18913829
· Installation Guide: INSTALL.md
· API Documentation: https://coralcore.netlify.app/api

---

For support: gitdeeper@gmail.com
ORCID: 0009-0003-8903-0029
DOI: 10.5281/zenodo.18913829
Web: coralcore.netlify.app

---

Last updated: 2026-03-09
