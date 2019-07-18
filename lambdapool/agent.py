'''
lambda_handler.agent

This module is the agent which is copied over to the lambda function and
acts as an entrypoint to the function package.

'''
import importlib
import base64
import cloudpickle

VERSION = '0.9.7'

def load_function(module_name: str, function_name: str):
    '''Loads a function from a module
    '''
    module = importlib.import_module(module_name)
    return getattr(module, function_name)

def lambda_handler(event: dict, context: dict):
    '''Entrypoint to handle the function invokation

    The `event` would be of the format:

    <encoded cloudpickle>

    Decoding the payload would result in a dictionary of the format:
    {
        "function": <function increment>,
        "args": [1],
        "kwargs": {"step": 5}
    }

    The handler then loads the module specified and runs the function
    with the given args and kwargs.

    Response Format
    ---
    dict

    {
        'result': <encoded cloudpickle>  # Only if no error occured.
        'error': 'error message string'  # If an error was caught during execution
    }

    All other exceptions which were caught by the AWS infrastructure, go in the
    format of AWS. These are handled by the client appropriately.
    '''
    payload = cloudpickle.loads(base64.b64decode(event))

    func = payload['function']
    args = payload['args']
    kwargs = payload['kwargs']

    response = {}
    try:
        result = func(*args, **kwargs)
        # serialize and pickle result
        result = base64.b64encode(cloudpickle.dumps(result)).decode('ascii')
        response['result'] = result
    except Exception as e:
        # return {'error': str(e)}
        response['error'] = str(e)

    return response
