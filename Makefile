.PHONY: all build test lint security

all: build test lint security

build:
	docker-compose -f infrastructure/docker-compose.yml build

test:
	@echo "Running all tests..."
	cd services/tracking && hatch run pytest
	cd services/ingestion && hatch run pytest

lint:
	@echo "Linting code..."
	cd services/tracking && hatch run black src && hatch run isort src && hatch run flake8 src
	cd services/ingestion && hatch run black src && hatch run isort src && hatch run flake8 src

security:
	@echo "Running security checks..."
	trivy fs --exit-code 1 .
	snyk test --all-projects
