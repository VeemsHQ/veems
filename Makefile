.ONESHELL:
.PHONY: lint
lint:
	flake8

.ONESHELL:
.PHONY: test
test:
	pytest -n auto -k 'not TestTranscode' --cov=.

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
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_STATIC}
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_MEDIA}

.ONESHELL:
.PHONY: run
run:
	docker-compose build app
	docker-compose run app

.ONESHELL:
.PHONY: docker-test
docker-test:
	docker-compose build app && docker-compose run app make test
