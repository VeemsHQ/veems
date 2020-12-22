.ONESHELL:
.PHONY: lint
lint:
	flake8

.ONESHELL:
.PHONY: test
test: install start-deps lint
	pytest -n auto --cov=. -vvv

.ONESHELL:
.PHONY: system_install
system_install:
	apt update && apt install -y ffmpeg

.ONESHELL:
.PHONY: test
install:
	pip install -r requirements-dev.txt

.ONESHELL:
start-deps:
	docker-compose up -d postgres rabbit localstack
	sleep 10
	aws --endpoint-url=${AWS_S3_ENDPOINT_URL} s3 mb s3://${BUCKET_STATIC}
	aws --endpoint-url=${AWS_S3_ENDPOINT_URL} s3 mb s3://${BUCKET_MEDIA}

.ONESHELL:
.PHONY: run
run:
	docker-compose build app
	docker-compose run app

.ONESHELL:
.PHONY: docker-test
docker-test:
	docker-compose build app && docker-compose run app make test
