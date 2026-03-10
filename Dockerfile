# 🪸 CORAL-CORE Docker Production Image
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

# =============================================================================
# BASE IMAGE
# =============================================================================
FROM python:3.10-slim-bullseye AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

# Set working directory
WORKDIR /app

# =============================================================================
# BUILDER STAGE
# =============================================================================
FROM base AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    curl \
    wget \
    git \
    libffi-dev \
    libssl-dev \
    libhdf5-dev \
    libnetcdf-dev \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libsndfile1-dev \
    libportaudio2 \
    portaudio19-dev \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python build dependencies
RUN pip install --upgrade pip setuptools wheel cython numpy

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# =============================================================================
# RUNTIME STAGE
# =============================================================================
FROM base AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-103 \
    libnetcdf19 \
    libopenblas0 \
    liblapack3 \
    libatlas3-base \
    libsndfile1 \
    libportaudio2 \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1000 coralcore && \
    useradd -u 1000 -g coralcore -s /bin/bash -m coralcore && \
    mkdir -p /data /logs /config && \
    chown -R coralcore:coralcore /app /data /logs /config

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install Python packages
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY --chown=coralcore:coralcore . /app

# Create necessary directories
RUN mkdir -p /data/raw /data/processed /data/backup /data/archive && \
    mkdir -p /logs/sensors /logs/app /logs/web && \
    mkdir -p /config/sensors /config/models && \
    chown -R coralcore:coralcore /data /logs /config

# Switch to non-root user
USER coralcore

# Set environment variables
ENV DATA_DIR=/data \
    LOG_DIR=/logs \
    CONFIG_DIR=/config \
    FLASK_ENV=production \
    FLASK_APP=/app/web/app.py

# Expose ports
EXPOSE 5000 8000 8080 8888

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Set entrypoint
ENTRYPOINT ["python", "-m", "coralcore.cli"]

# Default command
CMD ["serve", "--host", "0.0.0.0", "--port", "5000"]

# =============================================================================
# DEVELOPMENT STAGE
# =============================================================================
FROM runtime AS development

# Switch to root for dev dependencies
USER root

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    htop \
    tmux \
    curl \
    wget \
    git \
    iputils-ping \
    net-tools \
    telnet \
    gdb \
    strace \
    valgrind \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Switch back to coralcore user
USER coralcore

# Set development environment
ENV FLASK_ENV=development \
    FLASK_DEBUG=1 \
    PYTHONPATH=/app

# Development command
CMD ["serve", "--host", "0.0.0.0", "--port", "5000", "--debug"]

# =============================================================================
# GPU STAGE
# =============================================================================
FROM runtime AS gpu

# Switch to root
USER root

# Install CUDA support
RUN apt-get update && apt-get install -y --no-install-recommends \
    nvidia-cuda-toolkit \
    && rm -rf /var/lib/apt/lists/*

# Install GPU Python packages
RUN pip install --no-cache-dir \
    cupy-cuda11x \
    cudf \
    cuml \
    tensorrt

# Switch back to coralcore user
USER coralcore

# Set GPU environment
ENV CUDA_VISIBLE_DEVICES=0 \
    TF_GPU_ALLOCATOR=cuda_malloc_async

# =============================================================================
# SENSOR STAGE
# =============================================================================
FROM runtime AS sensor

# Switch to root
USER root

# Install sensor dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    usbutils \
    udev \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

# Add udev rules for sensors
COPY config/99-sensors.rules /etc/udev/rules.d/

# Install sensor Python packages
RUN pip install --no-cache-dir \
    pyserial \
    pyusb \
    pyvisa \
    pyvisa-py \
    sami-alk-driver \
    amar-g4-driver \
    diving-pam-driver \
    rdi-adcp-driver \
    sbe37-driver

# Switch back to coralcore user
USER coralcore

# Create sensor data directories
RUN mkdir -p /data/sensors/{sami,amar,pam,adcp,sbe37}

# =============================================================================
# TEST STAGE
# =============================================================================
FROM runtime AS test

# Switch to root
USER root

# Install test dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy test files
COPY --chown=coralcore:coralcore tests/ /app/tests/

# Switch to coralcore user
USER coralcore

# Run tests
CMD ["pytest", "tests/", "-v", "--cov=coralcore", "--cov-report=term"]

# =============================================================================
# DOCS STAGE
# =============================================================================
FROM runtime AS docs

# Switch to root
USER root

# Install documentation tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    texlive-latex-base \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

# Install documentation Python packages
COPY requirements-docs.txt .
RUN pip install --no-cache-dir -r requirements-docs.txt

# Copy documentation source
COPY --chown=coralcore:coralcore docs/ /app/docs/

# Build documentation
RUN cd docs && make html

# Switch to coralcore user
USER coralcore

# Command to serve documentation
CMD ["python", "-m", "http.server", "8000", "--directory", "docs/_build/html"]

# =============================================================================
# LABELS
# =============================================================================
LABEL maintainer="Samir Baladi <gitdeeper@gmail.com>" \
      org.opencontainers.image.title="CORAL-CORE" \
      org.opencontainers.image.description="Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.url="https://github.com/gitdeeper8/coralcore" \
      org.opencontainers.image.documentation="https://coralcore.netlify.app/docs" \
      org.opencontainers.image.source="https://github.com/gitdeeper8/coralcore.git" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.doi="10.5281/zenodo.18913829" \
      org.opencontainers.image.authors="Samir Baladi" \
      org.opencontainers.image.vendor="CORAL-CORE Project" \
      org.opencontainers.image.created="2026-03-08"

# =============================================================================
# END OF DOCKERFILE
# =============================================================================
