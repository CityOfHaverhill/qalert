start-local-services:
	docker-compose -f tests/docker-compose.yml up -d
	./tests/wait_for_postgres.sh

stop-local-services:
	docker-compose -f tests/docker-compose.yml down

run-function: start-local-services
	sam build --use-container
	sam local invoke --env-vars tests/local_config.json --docker-network haverhill_qalert_network

unit-tests: start-local-services
	pytest tests/unit

integration-tests: start-local-services
	pytest tests/integration

lint:
	flake8 haverhill_311_function/ tests/ 

all-tests: unit-tests integration-tests