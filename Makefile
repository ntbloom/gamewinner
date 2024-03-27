PYTEST_FLAGS = -s
PYTEST_FLAGS+= -x
PYTEST_FLAGS+= --cov=gamewinner/
PYTEST_FLAGS+= --show-capture=no
PYTEST_FLAGS+= --cov-report term-missing

.PHONY:install
install:
	python3 -m pip install poetry
	poetry install

.PHONY:test
test:
	poetry run pytest $(PYTEST_FLAGS)

.PHONY:precommit
precommit:
	poetry run pre-commit run --all-files

.PHONY:mypy
mypy:
	poetry run mypy .

.PHONY:docker
DOCKER_FLAGS=-f docker/docker-compose.yaml
docker:
	docker compose ${DOCKER_FLAGS} up --build

clean:
	rm -rf gamewinner/generated/*.bkt