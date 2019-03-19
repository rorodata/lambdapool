import pytest
from click.testing import CliRunner

from lambdapool.cli import cli
from lambdapool.aws import LambdaFunction

ECHO_CODE = '''
def echo(msg):
    return f'ECHOING: {msg}'
'''

@pytest.mark.aws
class TestCli:
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

    @pytest.fixture
    def function(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code == 0

    def test_create_function(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code == 0
        assert 'Succesfully created lambdapool function test-function' in result.output

    def test_list_no_functions(self):
        result = self.runner.invoke(cli, 'list')
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == 3

    def test_update_function_does_not_exist(self):
        result = self.runner.invoke(cli, ['update', 'test-function', 'test.py'])
        assert result.exit_code != 0
        assert 'test-function does not exist' in result.output

    def test_delete_function(self, function):
        result = self.runner.invoke(cli, ['delete', 'test-function'])
        assert result.exit_code == 0
        assert 'Deleted lambdapool function test-function' in result.output

    def test_delete_function_does_not_exist(self):
        result = self.runner.invoke(cli, ['delete', 'test-function'])
        assert result.exit_code != 0
        assert 'test-function does not exist' in result.output
