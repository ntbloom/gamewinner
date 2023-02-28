test:
	poetry run pytest

precommit:
	poetry run pre-commit run --all-files

mypy:
	poetry run mypy .
