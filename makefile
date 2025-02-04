PYTHON_FILES = $(shell find . -name "*.py" -not -path "./.venv/*")

local_setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements/dev/requirements.txt

local_clean:
	rm -rf .venv

local_run:
	fastapi dev main.py

up:
	docker-compose up --build -d

down:
	docker-compose down

check:
	@echo "🔧 Formateando código con Black..."
	black $(PYTHON_FILES)
	@echo "🔍 Analizando código con Flake8..."
	flake8 $(PYTHON_FILES)
	@echo "📊 Verificando tipos con MyPy..."
	mypy $(PYTHON_FILES)

logs:
	docker-compose logs -f

test:
	pytest -s


.PHONY: help

help:
	@echo "Commands:"
	@echo "  local_setup: Creates a virtual environment and installs the dependencies."
	@echo "  local_clean: Removes the virtual environment."
	@echo "  local_run: Starts the application locally."
	@echo "  up: Starts application containers."
	@echo "  down: Stops application containers."
	@echo "  check: Formats the code using black, verifies types with mypy and linting with flake8."
	@echo "  logs: Shows the logs of the application."
	@echo "  test: Runs unit tests."
	@echo "  help: Shows this help."
