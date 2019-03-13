import json
import logging
from multiprocessing.pool import ThreadPool
from typing import List

import boto3

from lambdapool.exceptions import LambdaPoolError

logger = logging.getLogger(__name__)

class Context:
    def __init__(self, lambda_function: str, aws_access_key_id: str, aws_secret_access_key: str, aws_region_name: str):
        self.lambda_function = lambda_function
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = aws_region_name

class LambdaFunction:
    def __init__(self, context, function_name):
        self.context = context
        self.function_name = function_name

    def __call__(self, *args, **kwargs):
        payload = {
            'function': self.function_name,
            'args': args,
            'kwargs': kwargs
        }

        return self._invoke_function(payload)

    def _invoke_function(self, payload):
        logger.info(f"=== Invoking {self.function_name} for {payload}")

        lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=self.context.aws_access_key_id,
            aws_secret_access_key=self.context.aws_secret_access_key,
            region_name=self.context.region_name,
        )


        response = lambda_client.invoke(
            FunctionName=self.context.lambda_function,
            LogType='Tail',
            Payload=json.dumps(payload).encode('ascii')
        )

        response_payload = json.loads(response['Payload'].read().decode('ascii'))

        if response_payload.get('error'):
            raise LambdaPoolError(response_payload['error'])
        # AWS errors like timeout errors are passed like this
        elif response_payload.get('errorMessage'):
            raise LambdaPoolError(response_payload['errorMessage'])

        result = response_payload['result']

        logger.info(f"=== Result for invokation of {self.function_name} on {payload}: {result}")

        return result

class LambdaPool:
    def __init__(self, workers: int, lambda_function: str, aws_access_key_id: str=None, aws_secret_access_key: str=None, region_name: str=None):
        self.workers = workers
        self.pool = ThreadPool(self.workers)
        self.context = Context(lambda_function, aws_access_key_id, aws_secret_access_key, region_name)

    def map(self, function: str, iterable: List):
        f = LambdaFunction(self.context, function)
        return self.pool.map(f, iterable)

    def apply(self, function: str, args: List = [], kwds: dict = {}):
        f = LambdaFunction(self.context, function)
        return f(*args, **kwds)

    def apply_async(self, function: str, args: List = [], kwds: dict = {}):
        f = LambdaFunction(self.context, function)
        return self.pool.apply_async(f, args=args, kwds=kwds)
