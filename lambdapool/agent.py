import importlib

class LambdaHandler:
    def __init__(self, package):
        self.package = package

    def __call__(self, event, context):
        module_name, _, function_name = event['function'].rpartition('.')
        args = event['args']
        kwargs = event['kwargs']

        func = load_function(module_name, function_name)
        return func(*args, **kwargs)

    def load_function(self, module_name, function_name):
        module = importlib.import_module('.' + module_name, self.package)
        return getattr(module, function_name)
