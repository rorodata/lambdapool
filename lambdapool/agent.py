import importlib

VERSION = '0.7.0'

def load_function(module_name, function_name):
    module = importlib.import_module(module_name)
    return getattr(module, function_name)

def lambda_handler(event, context):
    module_name, _, function_name = event['function'].rpartition('.')
    args = event['args']
    kwargs = event['kwargs']

    try:
        func = load_function(module_name, function_name)
    except (ModuleNotFoundError, AttributeError) as e:
        return {'error': str(e)}

    try:
        result = func(*args, **kwargs)
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}
