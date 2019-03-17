#! /bin/bash

export AWS_DEFAULT_REGION=us-west-2

pytest --flakes lambdapool
pytest --cov=lambdapool tests "$@"
