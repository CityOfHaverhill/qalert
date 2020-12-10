DB_HOST ?= localhost
DB_PORT ?= 5432
DB_USER ?= docker
DB_PASSWORD ?= docker
DB_DATABASE ?= qalert_test


start-local-services:
	docker-compose -f tests/docker-compose.yml up -d
	./tests/wait_for_postgres.sh

stop-local-services:
	docker-compose -f tests/docker-compose.yml down

db-revision:
	export DB_HOST=$(DB_HOST) && \
	export DB_PORT=$(DB_PORT) && \
	export DB_USER=$(DB_USER) && \
	export DB_PASSWORD=$(DB_PASSWORD) && \
	export DB_DATABASE=${DB_DATABASE} && \
	export PYTHONPATH=. && \
	alembic revision --autogenerate -m "$(MESSAGE)"

db-upgrade:
	export DB_HOST=$(DB_HOST) && \
	export DB_PORT=$(DB_PORT) && \
	export DB_USER=$(DB_USER) && \
	export DB_PASSWORD=$(DB_PASSWORD) && \
	export DB_DATABASE=${DB_DATABASE} && \
	export PYTHONPATH=. && \
	alembic upgrade head

run-function: start-local-services db-upgrade
	sam build --use-container
	sam local invoke --env-vars tests/local_config.json --docker-network haverhill_qalert_network

unit-tests: start-local-services
	pytest tests/unit

integration-tests: start-local-services
	pytest tests/integration

lint:
	flake8 haverhill_311_function/ tests/ 

all-tests: unit-tests integration-tests