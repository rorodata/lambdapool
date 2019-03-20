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

        with open('requirements.txt', 'w') as f:
            f.write('requests\n')

    @pytest.fixture
    def function(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code == 0

    def test_create_function_success(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code == 0
        assert 'Succesfully created lambdapool function test-function' in result.output

    def test_create_function_exists_error(self, function):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py'])
        assert result.exit_code != 0
        print(result.output)
        assert 'lambdapool function test-function already exists' in result.output

    def test_create_function_with_requirements(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--requirements', 'requirements.txt'])
        assert result.exit_code == 0
        assert 'Succesfully created lambdapool function test-function' in result.output

    def test_create_function_with_memory_success(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--memory', '192'])
        assert result.exit_code == 0
        assert 'Succesfully created lambdapool function test-function' in result.output

        result = self.runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert '192' in result.output

    def test_create_function_with_memory_failed(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--memory', '0'])
        assert result.exit_code != 0
        assert 'Invalid memory size provided' in result.output

        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--memory', '163'])
        assert result.exit_code != 0
        assert 'Invalid memory size provided' in result.output

        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--memory', '4096'])
        assert result.exit_code != 0
        assert 'Invalid memory size provided' in result.output

    def test_create_function_with_timeout_success(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--timeout', '300'])
        assert result.exit_code == 0
        assert 'Succesfully created lambdapool function test-function' in result.output

        result = self.runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert '300' in result.output

    def test_create_function_with_timeout_failed(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--timeout', '0'])
        assert result.exit_code != 0
        assert 'Invalid timeout provided' in result.output

        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--timeout', '901'])
        assert result.exit_code != 0
        assert 'Invalid timeout provided' in result.output

    def test_create_function_with_all_parameters(self, function_code):
        result = self.runner.invoke(cli, ['create', 'test-function', 'echo.py', '--requirements', 'requirements.txt', '--memory', '192', '--timeout', '300'])
        assert result.exit_code == 0
        assert 'Succesfully created lambdapool function test-function' in result.output

        result = self.runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert '192' in result.output
        assert '300' in result.output

    def test_list_no_functions(self):
        result = self.runner.invoke(cli, 'list')
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == 3

    def test_list_function_exists(self, function):
        result = self.runner.invoke(cli, 'list')
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == 4

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
