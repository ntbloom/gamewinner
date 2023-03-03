test:
	poetry run pytest -sx --cov=gamewinner/

precommit:
	poetry run pre-commit run --all-files

mypy:
	poetry run mypy .
