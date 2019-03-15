import os
import sys
import pathlib
import tempfile
import shutil

from lambdapool import utils, aws, exceptions

class LambdaPoolFunction:
    def __init__(self, function_name, memory, timeout, paths=None, requirements=None):
        self.function_name = function_name

        self.memory = memory
        self.timeout = timeout
        self.validate_function_configuration()

        self.paths = paths
        self.requirements = requirements
        self.resolve_paths()

    def resolve_paths(self):
        root = os.getcwd()
        self.paths = [
            pathlib.Path(root+'/'+path).resolve()
            for path in self.paths
        ] if self.paths else None
        self.requirements = pathlib.Path(root+'/'+self.requirements).resolve() if self.requirements else None

    def validate_function_configuration(self):
        if (self.memory is not None) and not self.validate_memory():
            raise exceptions.LambdaFunctionError('Invalid memory size provided. It should be in between 128MB to 3008MB, in 64MB increments')

        if (self.timeout is not None) and not self.validate_timeout():
            raise exceptions.LambdaFunctionError('Invalid timeout provided. It should be less than 900 seconds.')

    def validate_memory(self):
        return (self.memory >= 128) and (self.memory%64 == 0) and (self.memory <= 3008)

    def validate_timeout(self):
        return (self.timeout > 0) and (self.timeout <= 900)

    def create(self):
        if self.exists():
            print(f'=== LambdaPool function {self.function_name} already exists ===')
            sys.exit(1)

        with tempfile.TemporaryDirectory() as self.tempdir:
            self.copy_paths()
            self.install_requirements()

            with tempfile.NamedTemporaryFile() as self.temparchive:
                self.archive_function()
                self.create_function()

    def update(self):
        if not self.exists():
            print(f'=== LambdaPool function {self.function_name} does not exist ===')
            sys.exit(1)

        with tempfile.TemporaryDirectory() as self.tempdir:
            self.copy_paths()
            self.install_requirements()

            with tempfile.NamedTemporaryFile() as self.temparchive:
                self.archive_function()
                self.update_function()

    def delete(self):
        if not self.exists():
            print(f'=== LambdaPool function {self.function_name} does not exist ===')
            sys.exit(1)

        aws_lambda_function = aws.LambdaFunction(self.function_name)
        aws_lambda_function.delete()

    def exists(self):
        aws_lambda_function = aws.LambdaFunction(self.function_name)
        return aws_lambda_function.exists()

    def copy_paths(self):
        print('=== Copying all specified files and directories ===')

        for path in self.paths:
            dest = pathlib.Path(self.tempdir+'/'+path.name)
            print(f'Copying {path.name}...')
            utils.copy(path, dest)

        print('=== Copied all specified files and directories ===')

    def install_requirements(self):
        if self.requirements:
            packages = self.read_requirements()
            print(f'=== Installing requirements from {self.requirements} ===')
            for package in packages:
                self.install_package(package)
            print(f'=== Installed requirements from {self.requirements} ===')

        print(f'=== Installing lambdapool ===')
        self.install_package('git+ssh://git@gitlab.com/rorodata/lambdapool')
        print(f'=== Installed lambdapool ===')

    def read_requirements(self):
        print(f'=== Reading requirements from {self.requirements} ===')
        with self.requirements.open() as r:
            return [l.strip('\n') for l in r.readlines()]

    def install_package(self, package):
        command = f'pip install {package} --target {self.tempdir}'
        utils.run_command(command)

    def archive_function(self):
        print(f'=== Archiving selected files and directories ===')
        self.archive = shutil.make_archive(self.temparchive.name, 'zip', self.tempdir)

    def create_function(self):
        print(f'=== Uploading function and dependencies ===')

        with open(self.archive, 'rb') as f:
            archive_data = f.read()

        aws_lambda_function = aws.LambdaFunction(self.function_name, self.memory, self.timeout)
        aws_lambda_function.create(archive_data)

        print(f'=== Function {self.function_name} uploaded along with all dependencies ===')

    def update_function(self):
        print(f'=== Uploading function and dependencies ===')

        with open(self.archive, 'rb') as f:
            archive_data = f.read()

        aws_lambda_function = aws.LambdaFunction(self.function_name, self.memory, self.timeout)
        aws_lambda_function.update(archive_data)

        print(f'=== Function {self.function_name} uploaded along with all dependencies ===')

    @staticmethod
    def list():
        return aws.list_functions()
