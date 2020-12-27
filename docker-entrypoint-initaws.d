#!/bin/bash
set -x
awslocal s3 mb s3://veems-local-static-yourname
awslocal s3 mb s3://veems-local-media-yourname
set +x
