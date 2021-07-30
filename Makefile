BIN=venv/bin/
PYTHON=.$(BIN)/python
BASE_REQUIREMENTS = requirements/requirements-base.in
DEV_REQUIREMENTS = requirements/requirements-dev.in
ENV_NAME = reports

conda_create:
	conda create -n $(ENV_NAME) -y

conda_update:
	conda env update -n $(ENV_NAME) --file environment.yml  --prune

venv:
	python -m venv venv

clean:
	rm -rf venv
	find . -name "*.pyc" -exec rm -f {} \;

install_requirements:
	$(BIN)pip install -r $(BASE_REQUIREMENTS)

install_dev_requirements: install_requirements
	$(BIN)pip install -r $(DEV_REQUIREMENTS)

# Run unittests and generate html coverage report
test:
	coverage run --source=./src -m pytest tests
	coverage html

# Run linters check only
lint:
	$(BIN)isort . --check
	$(BIN)black . --check

# Run linters and try to fix the errors
format:
	$(BIN)isort .
	$(BIN)black .

# Update all libraries required to run this application
requirements_txt:
	sort -u $(BASE_REQUIREMENTS) -o $(BASE_REQUIREMENTS)
	pip-compile --output-file=requirements.txt $(BASE_REQUIREMENTS)

requirements_dev_txt:
	sort -u $(DEV_REQUIREMENTS) -o $(DEV_REQUIREMENTS)
	sort -u $(BASE_REQUIREMENTS) -o $(BASE_REQUIREMENTS)
	pip-compile --output-file=requirements-dev.txt $(BASE_REQUIREMENTS) $(DEV_REQUIREMENTS)

# Re/install the virtual environment with all requirements
install: clean venv install_requirements

# Re/install the virtual environment for DEV usage
dev_install: clean venv install_dev_requirements

# Do all checks
build: dev_install lint test
