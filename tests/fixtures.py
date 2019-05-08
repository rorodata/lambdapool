import pytest
from click.testing import CliRunner

from lambdapool.cli import cli
from lambdapool.aws import LambdaFunction, Role

ECHO_CODE = '''
def echo(msg):
    return f'ECHOING: {msg}'
'''

FIBONACCI_CODE = '''
def fib(n):
    if n>50: raise ValueError
    if n==0 or n==1: return n
    return fib(n-1) + fib(n-2)

'''

class TestFunctionBase:
    def teardown_method(self):
        lambda_function = LambdaFunction('test-function')
        if lambda_function.exists():
            lambda_function.delete()

    def ensure_clean_slate(self):
        lambda_function = LambdaFunction('test-function')
        if lambda_function.exists():
            lambda_function.delete()

        lambda_role = Role('lambdapool-role-test-function')
        if lambda_role.exists():
            lambda_role.delete()

    @pytest.fixture(autouse=True)
    def runner(self):
        self.runner = CliRunner()
        self.ensure_clean_slate()

    @pytest.fixture
    def runner_isolated_filesystem(self):
        with self.runner.isolated_filesystem():
            yield

    @pytest.fixture
    def function_code(self, runner_isolated_filesystem):
        with open('echo.py', 'w') as f:
            f.write(ECHO_CODE)

        with open('algorithms.py', 'w') as f:
            f.write(FIBONACCI_CODE)

        with open('requirements.txt', 'w') as f:
            f.write('requests\n')

    @pytest.fixture
    def function(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code == 0

    @pytest.fixture
    def function_fib(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'algorithms.py'])
        assert result.exit_code == 0
