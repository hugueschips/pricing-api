prepare-dev:
	poetry install

install:
	poetry install

check:
	poetry run black --check src/
	poetry run flake8

run:
	poetry run start

lint:
	poetry run black src/ tests/
	poetry run flake8
	poetry run isort src/ tests/

flake:
	poetry run flake8

docker-build-image:
	docker build -t pricing . --progress=plain

docker-deploy:
	docker run --rm -p 8007:80 pricing                                                                      

docker-deploy-dev:
	export DEPLOY_ENV=dev && set -a && . ${PWD}/.env.dev.docker && set +a && docker stack deploy -c docker-compose.yml pricing --prune