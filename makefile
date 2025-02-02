PYTHON_FILES = $(shell find . -name "*.py" -not -path "./.venv/*")

up:
	docker-compose up --build -d

down:
	docker-compose down

format:
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
	@echo "Comandos:"
	@echo "  up: Levanta los contenedores de la aplicación."
	@echo "  format: Formatea el código Python con black, ejecuta la verificación de tipos con mypy y el linting con flake8."
	@echo "  test: Ejecuta los tests unitarios."
	@echo "  coverage: Ejecuta los tests y genera un reporte de cobertura."
	@echo "  help: Muestra esta ayuda."
