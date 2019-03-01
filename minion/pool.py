import functools
import json
import logging
from multiprocessing.pool import Pool
from typing import List

import boto3

logger = logging.getLogger(__name__)

class LambdaPool:
    def __init__(self, workers: int, lambda_function: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, endpoint_url: str):
        self.workers = workers
        self.pool = Pool(self.workers)
        self.lambda_function = lambda_function
        self.lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            endpoint_url=endpoint_url
        )

    def map(self, function: str, parameters: List[dict]):
        f = functools.partial(self.invoke_function, self.lambda_function)
        payloads = [
            json.dumps({
                'function': function,
                'args': parameter.get("args", []),
                'kwargs': parameter.get("kwargs", {})
            }) for parameter in parameters
        ]
        self.pool.map(f, payloads)

    def apply(self, function: str, args: List = [], kwargs: dict = {}):
        f = functools.partial(self.invoke_function, self.lambda_function)
        payload = json.dumps({
            'function': function,
            'args': args,
            'kwargs': kwargs
        })
        return self.pool.apply(f, args=(payload,))

    def invoke_function(lambda_function: str, payload: dict):
        logger.info(f"=== Invoked {lambda_function} for {payload}")

        response = self.lambda_client.invoke(
            FunctionName=self.lambda_function,
            LogType='Tail',
            Payload=payload.encode('ascii')
        )

        result = json.loads(response['Payload'].read())["result"]

        logger.info(f"=== Result for invokation of {function} on {parameter}: {result}")
        print(result)

        return result
