#! /bin/bash

pytest --flakes lambdapool
pytest --cov=lambdapool tests "$@"
