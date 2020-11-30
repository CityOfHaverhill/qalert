start-db:
	docker stop qalert_db_local || true && docker rm qalert_db_local || true
	docker build tests/ -f tests/Dockerfile.postgres -t custom_postgres:1.0
	docker run -d -p 5432:5432 --name=qalert_db_local custom_postgres:1.0

stop-db:
	docker kill qalert_db_local

run-function: start-db
	sam build --use-container
	sam local invoke --env-vars tests/local_config.json --docker-network host

unit-tests: start-db
	./tests/wait_for_postgres.sh
	pytest tests/unit

integration-tests: start-db
	./tests/wait_for_postgres.sh
	pytest tests/integration

lint:
	flake8 haverhill_311_function/ tests/ 

all-tests: unit-tests integration-tests