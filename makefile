PYTHON_FILES = $(shell find . -name "*.py" -not -path "./.venv/*")

up:
	docker-compose up --build -d

down:
	docker-compose down

check:
	@echo "🔍 Analizando código con Flake8..."
	flake8 $(PYTHON_FILES)
	@echo "🔧 Formateando código con Black..."
	black $(PYTHON_FILES)
	@echo "📊 Verificando tipos con MyPy..."
	mypy $(PYTHON_FILES)

test:
	pytest

coverage:
	pytest --cov=vw_challenge --cov-report=term --cov-report=html

.PHONY: help

help:
	@echo "Commands:"
	@echo "  up: Starts application containers."
	@echo "  down: Stops application containers."
	@echo "  check: Formats the code using black, verifies types with mypy and linting with flake8."
	@echo "  test: Runs unit tests."
	@echo "  coverage: Runs unit tests and generates a coverage report."
	@echo "  help: Shows this help."
