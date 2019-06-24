import json
import base64
import logging
import threading
from multiprocessing.pool import ThreadPool
from typing import List, Optional

import boto3
from botocore.client import Config
import cloudpickle

from lambdapool.exceptions import LambdaPoolError

logger = logging.getLogger(__name__)

class Context:
    def __init__(self, lambda_function: str, aws_access_key_id: Optional[str]=None, aws_secret_access_key: Optional[str]=None, aws_region_name: Optional[str]=None, **kwargs):
        self.lambda_function = lambda_function
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = aws_region_name
        self.read_timeout = kwargs.pop('read_timeout', 300)

class LambdaFunction:
    def __init__(self, context, function_name):
        self.context = context
        self.function_name = function_name
        self._d = threading.local()

    def __call__(self, *args, **kwargs):
        payload = {
            'function': self.function_name,
            'args': args,
            'kwargs': kwargs
        }

        return self._invoke_function(payload)

    @property
    def lambda_client(self):
        d = self._d
        if not hasattr(d, "lambda_client"):
            d.lambda_client = boto3.client(
                'lambda',
                aws_access_key_id=self.context.aws_access_key_id,
                aws_secret_access_key=self.context.aws_secret_access_key,
                region_name=self.context.region_name,
                config=Config(read_timeout=self.context.read_timeout)
                )
        return d.lambda_client

    def _invoke_function(self, payload):
        # logger.info(f"=== Invoking {self.function_name} for {payload}")

        payload = {
            'payload': base64.b64encode(cloudpickle.dumps(payload)).decode('ascii')
        }

        response = self.lambda_client.invoke(
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

        result = cloudpickle.loads((base64.b64decode(response_payload['result'].encode('ascii'))))

        # logger.info(f"=== Result for invokation of {self.function_name} on {payload}: {result}")

        return result

class LambdaPool:
    def __init__(
        self,
        workers: int,
        lambda_function: str,
        aws_access_key_id: str=None,
        aws_secret_access_key: str=None,
        aws_region_name: str=None
    ):
        self.workers = workers
        self.context = Context(lambda_function, aws_access_key_id, aws_secret_access_key, aws_region_name)

    def map(self, function: str, iterable: List):
        f = LambdaFunction(self.context, function)
        with ThreadPool(self.workers) as pool:
            return pool.map(f, iterable)

    def apply(self, function: str, args: List = [], kwds: dict = {}):
        f = LambdaFunction(self.context, function)
        return f(*args, **kwds)

    def apply_async(self, function: str, args: List = [], kwds: dict = {}):
        f = LambdaFunction(self.context, function)
        with ThreadPool(self.workers) as pool:
            return pool.apply_async(f, args=args, kwds=kwds)
