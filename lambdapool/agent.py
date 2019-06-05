import importlib
import base64
import cloudpickle

VERSION = '0.9.3'

def load_function(module_name, function_name):
    module = importlib.import_module(module_name)
    return getattr(module, function_name)

def lambda_handler(event, context):
    # deserialize pickled payload
    pickled_payload = event['payload']
    payload = cloudpickle.loads(base64.b64decode(pickled_payload.encode('ascii')))

    module_name, _, function_name = payload['function'].rpartition('.')
    args = payload['args']
    kwargs = payload['kwargs']

    try:
        func = load_function(module_name, function_name)
    except (ModuleNotFoundError, AttributeError) as e:
        return {'error': str(e)}

    try:
        result = func(*args, **kwargs)
        # serialize and pickle result
        result = base64.b64encode(cloudpickle.dumps(result)).decode('ascii')
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}
