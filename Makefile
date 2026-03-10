# 🪸 CORAL-CORE Makefile
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

.PHONY: help install dev test lint clean docker-build docker-up docker-down \
        deploy backup restore docs jupyter format check release

# =============================================================================
# VARIABLES
# =============================================================================
SHELL := /bin/bash
PROJECT_NAME := coralcore
PYTHON := python3
PIP := pip3
VERSION := 1.0.0
DOCKER_REGISTRY := ghcr.io/gitdeeper8
DOCKER_IMAGE := $(DOCKER_REGISTRY)/$(PROJECT_NAME)
COMMIT_HASH := $(shell git rev-parse --short HEAD 2>/dev/null || echo "dev")
BUILD_TIME := $(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
VENV_DIR := venv
VENV_BIN := $(VENV_DIR)/bin

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# =============================================================================
# HELP
# =============================================================================
help:
	@echo "$(BLUE)🪸 CORAL-CORE Makefile$(NC)"
	@echo "Version: $(VERSION)"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "  make install     - Install in development mode"
	@echo "  make install-dev - Install with development dependencies"
	@echo "  make install-all - Install all dependencies"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev         - Run development server"
	@echo "  make jupyter     - Start Jupyter Lab"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean build artifacts"
	@echo ""
	@echo "$(GREEN)Docker:$(NC)"
	@echo "  make docker-build   - Build Docker images"
	@echo "  make docker-up      - Start Docker services"
	@echo "  make docker-down    - Stop Docker services"
	@echo "  make docker-logs    - View Docker logs"
	@echo "  make docker-clean   - Clean Docker resources"
	@echo ""
	@echo "$(GREEN)Deployment:$(NC)"
	@echo "  make deploy          - Deploy to production"
	@echo "  make deploy-staging  - Deploy to staging"
	@echo "  make backup          - Create backup"
	@echo "  make restore         - Restore from backup"
	@echo ""
	@echo "$(GREEN)Documentation:$(NC)"
	@echo "  make docs        - Build documentation"
	@echo "  make docs-serve  - Serve documentation locally"
	@echo ""
	@echo "$(GREEN)Release:$(NC)"
	@echo "  make release     - Create new release"
	@echo "  make publish     - Publish to PyPI"

# =============================================================================
# INSTALLATION
# =============================================================================
install:
	@echo "$(BLUE)Installing CORAL-CORE in development mode...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .
	@echo "$(GREEN)✓ Installation complete$(NC)"

install-dev:
	@echo "$(BLUE)Installing with development dependencies...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
	@echo "$(GREEN)✓ Development installation complete$(NC)"

install-all:
	@echo "$(BLUE)Installing all dependencies...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[all]"
	@echo "$(GREEN)✓ All dependencies installed$(NC)"

# =============================================================================
# VIRTUAL ENVIRONMENT
# =============================================================================
venv:
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment created$(NC)"

venv-activate:
	@echo "$(YELLOW)Run: source $(VENV_DIR)/bin/activate$(NC)"

# =============================================================================
# DEVELOPMENT
# =============================================================================
dev:
	@echo "$(BLUE)Starting development server...$(NC)"
	FLASK_ENV=development FLASK_APP=web/app.py flask run --host=0.0.0.0 --port=5000

jupyter:
	@echo "$(BLUE)Starting Jupyter Lab...$(NC)"
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=''

test:
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v --cov=$(PROJECT_NAME) --cov-report=term --cov-report=html
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-quick:
	@echo "$(BLUE)Running quick tests...$(NC)"
	pytest tests/ -v -m "not slow"

test-field:
	@echo "$(BLUE)Running field data validation tests...$(NC)"
	pytest tests/ -v -m field

lint:
	@echo "$(BLUE)Running linters...$(NC)"
	flake8 $(PROJECT_NAME) tests
	pylint $(PROJECT_NAME) tests
	mypy $(PROJECT_NAME)
	@echo "$(GREEN)✓ Linting complete$(NC)"

format:
	@echo "$(BLUE)Formatting code...$(NC)"
	black $(PROJECT_NAME) tests
	isort $(PROJECT_NAME) tests
	@echo "$(GREEN)✓ Formatting complete$(NC)"

check: lint test
	@echo "$(GREEN)✓ All checks passed$(NC)"

# =============================================================================
# CLEAN
# =============================================================================
clean:
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf coverage.xml
	rm -rf *.pyc
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "$(GREEN)✓ Clean complete$(NC)"

clean-all: clean
	@echo "$(BLUE)Cleaning all...$(NC)"
	rm -rf $(VENV_DIR)/
	rm -rf data/raw/*
	rm -rf data/processed/*
	rm -rf logs/*
	rm -rf notebooks/.ipynb_checkpoints/
	docker system prune -f
	@echo "$(GREEN)✓ Clean all complete$(NC)"

# =============================================================================
# DOCKER
# =============================================================================
docker-build:
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker build -t $(PROJECT_NAME):$(VERSION) .
	docker build -t $(PROJECT_NAME):dev -f Dockerfile.dev .
	docker build -t $(PROJECT_NAME):gpu -f Dockerfile.gpu .
	@echo "$(GREEN)✓ Docker build complete$(NC)"

docker-build-production:
	@echo "$(BLUE)Building production Docker images...$(NC)"
	docker build \
		--build-arg VERSION=$(VERSION) \
		--build-arg COMMIT_HASH=$(COMMIT_HASH) \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		-f Dockerfile .
	@echo "$(GREEN)✓ Production build complete$(NC)"

docker-up:
	@echo "$(BLUE)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Docker services started$(NC)"

docker-down:
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Docker services stopped$(NC)"

docker-restart: docker-down docker-up
	@echo "$(GREEN)✓ Docker services restarted$(NC)"

docker-logs:
	docker-compose logs -f

docker-ps:
	docker-compose ps

docker-clean:
	@echo "$(BLUE)Cleaning Docker resources...$(NC)"
	docker-compose down -v
	docker system prune -f
	docker volume prune -f
	@echo "$(GREEN)✓ Docker clean complete$(NC)"

docker-shell:
	docker-compose exec $(SERVICE) /bin/bash

# =============================================================================
# DEPLOYMENT
# =============================================================================
deploy:
	@echo "$(BLUE)Deploying to production...$(NC)"
	@./scripts/deploy.sh production
	@echo "$(GREEN)✓ Deployment complete$(NC)"

deploy-staging:
	@echo "$(BLUE)Deploying to staging...$(NC)"
	@./scripts/deploy.sh staging
	@echo "$(GREEN)✓ Staging deployment complete$(NC)"

backup:
	@echo "$(BLUE)Creating backup...$(NC)"
	@./scripts/backup.sh
	@echo "$(GREEN)✓ Backup complete$(NC)"

restore:
	@echo "$(BLUE)Restoring from backup...$(NC)"
	@./scripts/restore.sh $(BACKUP)
	@echo "$(GREEN)✓ Restore complete$(NC)"

# =============================================================================
# DOCUMENTATION
# =============================================================================
docs:
	@echo "$(BLUE)Building documentation...$(NC)"
	cd docs && make html
	@echo "$(GREEN)✓ Documentation built at docs/_build/html$(NC)"

docs-serve:
	@echo "$(BLUE)Serving documentation at http://localhost:8000$(NC)"
	cd docs/_build/html && python -m http.server 8000

docs-deploy:
	@echo "$(BLUE)Deploying documentation...$(NC)"
	mkdocs gh-deploy --force
	@echo "$(GREEN)✓ Documentation deployed$(NC)"

# =============================================================================
# DATABASE
# =============================================================================
db-init:
	@echo "$(BLUE)Initializing database...$(NC)"
	$(PYTHON) scripts/init_db.py
	@echo "$(GREEN)✓ Database initialized$(NC)"

db-migrate:
	@echo "$(BLUE)Running database migrations...$(NC)"
	alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(NC)"

db-reset:
	@echo "$(RED)Resetting database...$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(PYTHON) scripts/reset_db.py; \
		echo "$(GREEN)✓ Database reset$(NC)"; \
	fi

# =============================================================================
# RELEASE
# =============================================================================
release:
	@echo "$(BLUE)Creating release $(VERSION)...$(NC)"
	@git tag -a v$(VERSION) -m "Release version $(VERSION)"
	@git push origin v$(VERSION)
	@echo "$(GREEN)✓ Release created$(NC)"

publish:
	@echo "$(BLUE)Publishing to PyPI...$(NC)"
	$(PYTHON) setup.py sdist bdist_wheel
	twine upload dist/*
	@echo "$(GREEN)✓ Published to PyPI$(NC)"

publish-docker: docker-build-production
	@echo "$(BLUE)Publishing Docker images...$(NC)"
	docker push $(DOCKER_IMAGE):$(VERSION)
	docker push $(DOCKER_IMAGE):latest
	@echo "$(GREEN)✓ Docker images published$(NC)"

# =============================================================================
# UTILITIES
# =============================================================================
update-requirements:
	@echo "$(BLUE)Updating requirements.txt...$(NC)"
	pip freeze > requirements.txt
	@echo "$(GREEN)✓ Requirements updated$(NC)"

check-deps:
	@echo "$(BLUE)Checking for outdated dependencies...$(NC)"
	pip list --outdated
	@safety check

tree:
	@echo "$(BLUE)Project structure:$(NC)"
	tree -I 'venv|__pycache__|*.pyc|*.pyo|.git|.pytest_cache|.mypy_cache'

info:
	@echo "$(BLUE)CORAL-CORE Project Info$(NC)"
	@echo "Version: $(VERSION)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Git hash: $(COMMIT_HASH)"
	@echo "Build time: $(BUILD_TIME)"
	@echo "Working dir: $(shell pwd)"

# =============================================================================
# DEFAULT TARGET
# =============================================================================
.DEFAULT_GOAL := help
