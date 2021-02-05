#!/bin/bash
set -x
awslocal s3 mb s3://veems-local-static
awslocal s3 mb s3://veems-local-media
set +x
