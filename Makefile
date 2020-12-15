.ONESHELL:
.PHONY: lint
lint:
	flake8

.ONESHELL:
.PHONY: test
test:
	pytest -n auto --cov=.

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
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_UPLOADS}
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_MEDIA_FILES}
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_MEDIA_FILE_THUMBNAILS}

.ONESHELL:
.PHONY: run
run:
	docker-compose build app
	docker-compose run app

