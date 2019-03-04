import importlib

def load_function(module_name, function_name):
    module = importlib.import_module(module_name)
    return getattr(module, function_name)

def lambda_handler(event, context):
    module_name, _, function_name = event['function'].rpartition('.')
    args = event['args']
    kwargs = event['kwargs']

    func = load_function(module_name, function_name)

    return func(*args, **kwargs)
