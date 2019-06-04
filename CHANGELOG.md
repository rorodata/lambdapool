# CHANGELOG

## 0.9.2

- Changes Author Info and restructures `setup.py`

## 0.9.1

- Adds `cloudpickle` to the requirements

## 0.9.0

- Adds support for data serializing using cloudpickle
- Fixes multithreading quirks with boto3 client
- Minor bug fixes

## v0.8.0

- Improves the CLI with help text and better formatting
- Adds test and coverage infrastructure
- Adds tests for most of the codebase
- Adds option to specify memory and timeout while creating or updating functions
- Adds support for specifying layers to LambdaFunction's
- Implements LambdaExecutor

## v0.7.0

- Implements functionality to propagate and raise appropriate errors
- Changes the lambdapool function identification protocol to environment variables from tags
- Makes lambdapool list an O(1) operation from the existing O(n)
- Fixes an issue with AWS IAM role
- Fixes bugs with return result not being json decoded

## v0.6

- Implements lambdapool cli
- Adds `create`, `update`, `list`, `delete` cli command functionalities


## v0.5.1

- Fixes typo in lambdapool.agent.load_function

## v0.5

- Reverts back to the old style of lambda_handler

## v0.4.1

- Fixes typo in LambdaHandler

## v0.4

- Finalizes LambdaHandler API

## v0.3

- Finalizes LambdaPool API
- Changes the behavior of AWS Lambda handler function. It returns the function result as it is now.

## v0.2.1

- Minor changes to `lambdapool/__init__.py`

## v0.2.0

- Refactors the LambdaPool.apply API

## v0.1.1

- Minor refactors

## v0.1.0

- Initial code with the AWS Lambda agent and LambdaPool
