from typing import Iterable, Union, Any
from concurrent.futures import ThreadPoolExecutor

from .pool import Context, LambdaFunction

class LambdaExecutor:
    def __init__(self,
        lambda_function: str,
        aws_access_key_id: str=None,
        aws_secret_access_key: str=None,
        aws_region_name: str=None,
        max_workers: int=None
    ):
        self.max_workers = max_workers
        self.context = Context(lambda_function, aws_access_key_id, aws_secret_access_key, aws_region_name)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, function_name: str, *args: Any, **kwargs: Any):
        f = LambdaFunction(self.context, function_name)
        return self.executor.submit(f, *args, **kwargs)

    def map(self, function_name: str, iterable: Iterable, timeout: Union[int, float]=None):
        f = LambdaFunction(self.context, function_name)
        return self.executor.map(f, iterable)

    def shutdown(self, wait: bool=True):
        self.executor.shutdown(wait=wait)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.shutdown()
