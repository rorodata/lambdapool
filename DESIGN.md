# Lambda Pool

> Author: Nabarun Pal <nabarun@rorodata.com>

> Created: 28 Feb 2019

> Last Modified: 20 Jul 2019

## Overview

Lambda Pool constitutes a system where a developer can deploy code on AWS Lambda and use it easily with a simple and comprehendible interface without going too much out of way from existing code.

The other primary objective is to abstract away the process of creating a Lambda function which is also tedious and requires domain knowledge. The goal of this tool is to remove the requirement of domain knowledge when trying to use serverless technology in day to day developer workflow.

This documents outlines the goals and structure of the project.

## Context

The `algoshelf` stack of software needs a Task Queue to run data pipelines like forecast computation. The constituent tasks can be broken down into independent components which can be parallely scheduled. One way of doing this running the tasks on different machine cores using `multiprocessing`. But, this is not very scalable and leads to wastage of compute resources as the resources lie idle for most periods of time.

A better way to tackle the problem is to use serverless technology as a backend for running the computation. There are various serverless options in market pushed by the major cloud providers, for example, Amazon Web Services Lambda by Amazon and Google Cloud functions by Google. Serverless abstracts away the underlying compute resources. The users don't need to think about spawning infrastructure, scaling them up during high resource usage and scaling them back down when idle. The idea is to make running the compute workloads `virtually infinitely scalable` (subject to AWS limitations).

We will be focusing on AWS Lambda here.

## Goals

- Implement LambdaPool interface [#A]
- Implement the agent which sits inside a lambda function [#A]
- Design the structure which will be used to specify our functions [#A]
- Design CLI to create, list, update and delete functions [#A]
- Support for specifying function layers, list layers used foreach functions [#A]
- Executor Interface [#A]
- Permissions management system [#B]
- System to fetch execution logs [#B]
- Extend the system to GCF [#B]

[#X] = Priority

## Source Code

The source code for the above implementation can be found [here](https://gitlab.com/rorodata/lambdapool)

## Installation

You can try this out by installing it using `pip` from the `git` repo,

```bash
$ pip install --user git+https://gitlab.com/rorodata/lambdapool
```

> The above command would only work if you have access to the repository.

> The package would shortly be uploaded to PyPI. Till then, the above is the suggested way to install LambdaPool.

## Command Line Interface

`LambdaPool` ships with a CLI to manage the code uploaded to AWS Lambda. The tool allows you to create, delete, list and update Lambda functions.

```bash
$ lambdapool
Usage: lambdapool [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new function
  delete  Delete a function
  list    List all deployed functions
  update  Update an existing function
```

More information can be found regarding each of the above commands by `lambdapool <command> --help`

```bash
$ lambdapool create --help
Usage: lambdapool create [OPTIONS] FUNCTION_NAME [PATHS]...

  Create a new function

Options:
  -r, --requirements PATH  Specifies the dependencies to be installed along
                           with the function
  --memory INTEGER         Sets the memory size of the function environment
  --timeout INTEGER        Sets the timeout for the function in seconds
  --layers TEXT            Sets the layers to be used when the function is
                           ran. The Layers ARN's (a maximum of 5) should be
                           specified.
  --help                   Show this message and exit.
```

### <a name="deploy"></a> Deploying to Lambda

Any python module can be deployed to Lambda using the `create` command.

For example, let's take the below code:

```bash
$ tree algorithms/
algorithms
├── algorithms.py
└── __init__.py

$ cat algorithms/algorithms.py
def fibonacci(n):
    '''A naive implementation of computing n'th fibonacci number
    '''
    if n==0: return 0
    if n==1: return 1
    return fibonacci(n-1) + fibonacci(n-2)
```

The above can be deployed to lambda using:

```bash
$ lambdapool create algorithms algorithms/ --timeout=300 --memory=100
=== Creating lambdapool function ===
=== Copying all specified files and directories ===
Copying algorithms.py...
...
=== Succesfully created lambdapool function algorithms ===
```

The specified code is now uploaded to AWS Lambda as a Lambda function. This is now ready to be consumed in your code. The API for LambdaPool is explained below.

## Using the LambdaPool API

> Note: Make sure you deploy the lambda function before trying to invoke the function.

The user should be able to create a pool of workers, specifying the maximum concurrency. Also, LambdaPool would require the name of the Lambda function that sits as an entrypoint on AWS Lambda.

```python
>>> from lambdapool import LambdaPool
>>> pool = LambdaPool(
    workers=10,
    lambda_function='algorithms',
    aws_access_key_id='...',
    aws_secret_access_key='...',
    aws_region_name='...'
    )
```

> If the AWS credentials are not provided, system defaults are used.

Assuming the definition and signature of the fibonnaci function looks like this:

```python
# algorithms.py

def fibonacci(n):
    # Worst case implementation for fibonacci :)
    if n==0: return 0
    if n==1: return 1

    return fibonacci(n-1) + fibonacci(n-2)
```

The user can perform a single synchronous task like the following:

```python
>>> from algorithms.algorithms import fibonacci
>>> pool.apply(fibonacci, args=[10])
55
```

Or, you can specify keyword arguments instead also,

```python
>>> pool.apply(fibonacci, kwds={'n': 10})
55
```

An asynchronous invocation is possible as:

```python
>>> result = pool.apply_async(fibonacci, kwds={'n': 10})
>>> result
<class 'multiprocessing.pool.ApplyResult'>
>>> result.get()
55
```

The user can also use map to perform mutliple tasks at the same time.

```python
>>> pool.map(fibonacci, range(100))
[0, 1, 1, 2, 3, 5, 8, ...]
```

> Note: The `LambdaPool.map` interface does not support keyword arguments. Passing more than one argument is also not possible. This is a decision strictly taken to conform with `multiprocessing.pool.ThreadPool` [API](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool).

## Executor API

As noticed above, the `LambdaPool` API is limiting in a sense that we can't pass in more than one arguments or use keyword arguments while using the `map` construct.

Python 3.5 introduced a new interface to perform concurrent computing. This was named the `Executor` [API](https://docs.python.org/3/library/concurrent.futures.html#executor-objects). Concurrent workloads can be run on threads using `ThreadPoolExecutor` and on seperate processess using `ProcessPoolExecutor`.

LambdaPool also exposes a similar interface known as `LambdaExecutor`. It has the exact similar functions and function signatures to run python callables asynchronously. The initializer is a bit different.

```python
>>> from lambdapool import LambdaExecutor
>>> from algorithms.algorithms import fibonacci
>>> with LambdaExecutor(lambda_function='algorithms') as executor:
...    futures = [executor.submit(fibonacci, n) for n in range(100)]
...    fibonaccis = [f.result() for f in futures]

>>> fibonaccis
[0, 1, 1, 2, 3, 5, 8, ...]

```

The `submit` method returns what is known as a [Future](https://docs.python.org/3/library/concurrent.futures.html#future-objects) object. This follows the Python native way of handling the encapsulated data. `LambdaExecutor` is just a wrapper on top of the `ThreadPoolExecutor` interface providing the added features of invoking the functions on the AWS Lambda infrastructure and not on the client computer. This way very high levels of concurrency can be achieved.

> Note: The above example assumes that the functions are already deployed to Lambda, as shown [here](#deployment)

## Limitations

- Serialization of the payload is being a hurdle. Need to find better solutions than Cloudpickle.
- The decoupling between function provisioning and execution can cause incoherencies.

## Future Improvements

- Permissions management system
- System to fetch execution logs
- Extend the system to GCF

## Internals and Under the Hood

### Creating a Lambda function

When `create` is called from CLI, the following happens,

1. The arguments are checked for correctness.

    - Checked if one or more files and directories are specified.
    - The `timeout` should be a positive number less than 900. The maximum timout for a lambda function is 15minutes or 900seconds.
    - The `memory` should be in between 128(MB) and 3008(MB) and be a multiple of 64MB.
    - There is no validation to the `layers` arguments but should be implemented in future.
    - The `requirements` file is checked if it exists

1. The files and/or directories specified are copied to a temporary folder.
1. All packages from the specifies `requirements` are installed.
1. The agent script is copied and cloudpickle is installed.
1. The temporary directory is then archived into a ZIP.
1. The ZIP folder is uploaded to the AWS Lambda API along with the function configuration variables like memory, timeout and layer ARN's.
1. Some identifiable information is added to the function in the form of tags which makes information retrieval in future easier.

### Updating a Lambda function

The same happens as above. We need to make the process intelligent by detecting whether the configuration changes or the specified artefacts(files and/or directories). In either cases, we need to perform only that modification instead of updating function code as well as configuration right now.

### Listing all Lambda functions

The `list` command only lists the functions which have been created by lambdapool. This filtering is done using the identifiable tags created while creating a function.

### Deleting a Lambda function

This action simple deletes all the information associated with that function after verifying if it was created by lambdapool through the tags.

### Calling a function using either the Pool or the Executor API

The only difference between the Pool and the Executor interfaces are the in built differences which are present in their Pythonic counterparts.

Whenever a function is called using the interfaces,

1. The callable specified, positional arguments and the keyword arguments are serialized using cloudpickle.
1. The lambda function is then called using the boto3 `invoke` call, providing the pickle as the payload.
1. The agent uploaded along with the user code to the lambda function unpickles the payload and calls the callable passing it the positional and keyword arguments.
1. The results obtained are pickled and returned as the response.
1. The client then unpickles the response and checks if an error was raised by Lambda in the response. If there was no error, the user is presented with the result.
1. In case of errors, LambdaPool raises an appropriate exception class to be caught by the user. If an error was raised by the user code, `LambdaPoolError` is raised along with the error message. If the error was raised by AWS, `LambdaFunctionError` is raised with the error message.

## References

1. [AWS Lambda CLI Getting Started](https://docs.aws.amazon.com/lambda/latest/dg/with-userapp.html)
2. [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
3. [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

## Document Changelog

### 20 July 2019
-  Refactors the structure and adds content

### 3 March 2019
- Adds documentation about the handler

### 1 March 2019
- Finalizes LambdaPool API

### 28 Feb 2019
- Initial document
