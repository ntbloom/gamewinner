test:
	poetry run pytest -x --cov=gamewinner/

precommit:
	poetry run pre-commit run --all-files

mypy:
	poetry run mypy .
