import pytest
from click.testing import CliRunner

from lambdapool.cli import cli
from lambdapool.aws import LambdaFunction

ECHO_CODE = '''
def echo(msg):
    return f'ECHOING: {msg}'
'''

class TestFunctionBase:
    def teardown_method(self):
        lambda_function = LambdaFunction('test-function')
        if lambda_function.exists():
            lambda_function.delete()

    @pytest.fixture(autouse=True)
    def runner(self):
        self.runner = CliRunner()

    @pytest.fixture
    def runner_isolated_filesystem(self):
        with self.runner.isolated_filesystem():
            yield

    @pytest.fixture
    def function_code(self, runner_isolated_filesystem):
        with open('echo.py', 'w') as f:
            f.write(ECHO_CODE)

        with open('requirements.txt', 'w') as f:
            f.write('requests\n')

    @pytest.fixture
    def function(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code == 0
