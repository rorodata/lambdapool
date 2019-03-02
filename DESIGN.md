# Lambda Pool

> Author: Nabarun Pal <nabarun@rorodata.com>
> Reviewer: Anand Chitipothu <anand@rorodata.com>
> Created: 28 Feb 2019

## Overview

The idea is to have a piece of software which will execute pre-defined functions parallely. Those functions would be running on AWS Lambda.

## Context

The `algoshelf` stack of software needs a Task Queue to run tasks like `compute_forecast`, `prepare_planning_cycle` etc. Currently, the Task Queue implementation uses polling based loop to execute tasks. One other aspect of this is the ability to run the constituent logic of tasks like `compute_forecast`, `prepare_planning_cycle` etc. on a scalable pool of workers instead of running them on Process pools. The idea is to make them virtually infinitely scalable.

## Goals

- [ ] Implement LambdaPool interface
- [ ] Implement the agent which sits inside a lambda function
- [ ] ...

## LambdaPool - API

The user should be able to create a pool of workers, specifying concurrency. Also, LambdaPool would require the name of the Lambda function that sits as an entrypoint on AWS Lambda.

```python
>>> from lambdapool import LambdaPool
>>> pool = LambdaPool(
    workers=10,
    lambda_entrypoint='nabarun-math-helpers',
    aws_access_key_id='...',
    aws_secret_access_key='...',
    aws_region_name='...'
    )
```

> If the credentials are not provided, system defaults are used.

Assuming the definition and signature of the fibonnaci function looks like this:

```python
# math.py

def fibonacci(n):
    # Worst case implementation for fibonacci :)
    if n==0: return 0
    if n==1: return 1

    return fibonacci(n-1) + fibonacci(n-2)

```

The user can perform a single synchronous task like the following:

```python
>>> pool.apply('math.fibonacci', args=[10])
```

Or, you can specify keyword arguments instead also,

```python
>>> pool.apply('math.fibonacci', kwds={'n': 10})
```

An asynchronous invocation is possible as:

```python
>>> pool.apply_async('math.fibonacci', kwds={'n': 10})
<class 'multiprocessing.pool.ApplyResult'>
```

The user can also use map to perform mutliple tasks at the same time.

```python
>>> pool.map('math.fibonacci', range(100))
```

> Note: The `LambdaPool.map` interface does not support keyword arguments. Passing more than one argument is also not possible. This is a decision strictly taken to conform with `multiprocessing.pool.ThreadPool` API.

The source code for the above implementation can be found [here](lambda-pool-src)

You can try this out by installing it from `pip`,

```bash
$ pip install --user git+https://gitlab.com/rorodata/lambda-pool
```

> Note: But make sure you deploy the lambda function before using `lambda-pool`.

## Structure of the AWS Lambda artefacts

> Work In Progress


## TODO

- [ ] Research and formalizing the usage of AWS SAM (Serverless Application Model) templates
- [ ] Processing the return result from the function
- [ ] Logging inside the function
- [ ] Proper error handling
- [ ] Local development of the application

## References

1. [AWS Lambda CLI Getting Started](https://docs.aws.amazon.com/lambda/latest/dg/with-userapp.html)
2. [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
3. [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

## Changelog

### v0.2 - 1 March 2019

- Finalizes LambdaPool API

### v0.1 - 28 Feb 2019

- Initial document

[lambda-pool-src]: https://github.com/rorodata/lambda-pool
