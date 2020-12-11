.ONESHELL:
lint:
	flake8

.ONESHELL:
test:
	pytest --cov=.

.ONESHELL:
start-deps:
	docker-compose up -d postgres rabbit
	# aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_STATIC}
	# aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_UPLOADS}
	# aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_MEDIA_FILES}
	# aws --endpoint-url=http://localhost:4566 s3 mb s3://${BUCKET_MEDIA_FILE_THUMBNAILS}

.ONESHELL:
.PHONY: run
run:
	docker-compose build app
	docker-compose run app
