PYTEST_FLAGS = -s
PYTEST_FLAGS+= -x
PYTEST_FLAGS+= --cov=gamewinner/
PYTEST_FLAGS+= --show-capture=no
PYTEST_FLAGS+= --cov-report term-missing

install:
	python3 -m pip install poetry
	poetry install

test:
	poetry run pytest $(PYTEST_FLAGS)

precommit:
	poetry run pre-commit run --all-files

mypy:
	poetry run mypy .
