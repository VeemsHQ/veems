AWS_REGION=us-east-1

.ONESHELL:
lint:
	flake8

.ONESHELL:
test:
	pytest --cov=.

.ONESHELL:
start-deps:
	docker-compose up -d postgres localstack
	aws --endpoint-url=http://localhost:4566 s3 mb s3://veems-local
	aws --endpoint-url=http://localhost:4566 s3 mb s3://veems-local-uploaded

.ONESHELL:
.PHONY: run
run:
	docker-compose build app
	docker-compose run app
