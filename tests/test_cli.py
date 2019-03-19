import pytest
from click.testing import CliRunner

from lambdapool.cli import cli

@pytest.mark.aws
class TestCli:
    def test_list_no_functions(self):
        runner = CliRunner()
        result = runner.invoke(cli, 'list')
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == 3

    def test_delete_function_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['delete', 'test-function'])
        assert result.exit_code != 0
        assert 'test-function does not exist' in result.output

    def test_update_function_does_not_exist(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['update', 'test-function', 'test.py'])
        assert result.exit_code != 0
        assert 'test-function does not exist' in result.output
