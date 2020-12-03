AWS_REGION=us-east-1

lint:
	flake8

test:
	pytest --cov=.

start-deps:
	docker-compose up -d postgres localstack

.PHONY: run
run:
	docker-compose build app
	docker-compose run app
