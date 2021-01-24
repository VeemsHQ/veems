.ONESHELL:
.PHONY: lint
lint:
	flake8

.ONESHELL:
.PHONY: test
test: install lint
	pytest -n auto -k 'TestTranscode' -vvv
	pytest -n auto -k 'not TestTranscode' -vvv

.ONESHELL:
.PHONY: system_install
system_install:
	apt update && apt install -y ffmpeg

.ONESHELL:
.PHONY: test
install:
	pip install -r requirements-dev.txt

.ONESHELL:
make-buckets-remote:
	aws s3 mb s3://${BUCKET_STATIC}
	aws s3 mb s3://${BUCKET_MEDIA}

.ONESHELL:
start-deps-remote:
	docker-compose up -d postgres rabbit localstack

.ONESHELL:
start-deps:
	docker-compose up -d postgres rabbit localstack
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_STATIC}
	aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_MEDIA}

.ONESHELL:
.PHONY: reset
reset:
	python manage.py flush --noinput
	python manage.py import_seed_data

.ONESHELL:
.PHONY: run
run:
	docker-compose build app_local
	docker-compose run --service-port app_local

.ONESHELL:
.PHONY: run
run_seed:
	docker-compose build app_local
	docker-compose run --service-port app_local make install && make reset

.ONESHELL:
.PHONY: docker-test
docker-test:
	docker-compose build app_test
	docker-compose run app_test
