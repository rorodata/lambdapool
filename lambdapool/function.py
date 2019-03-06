import os
import pathlib
import tempfile
import shutil
import base64

from lambdapool import utils, aws

class LambdaFunction:
    def __init__(self, function_name, paths, requirements=None):
        self.function_name = function_name
        self.paths = paths
        self.requirements = requirements
        self.resolve_paths()

    def resolve_paths(self):
        root = os.getcwd()
        self.paths = [
            pathlib.Path(root+'/'+path).resolve()
            for path in self.paths
        ]
        self.requirements = pathlib.Path(root+'/'+self.requirements).resolve() if self.requirements else None

    def create(self):
        with tempfile.TemporaryDirectory() as self.tempdir:
            self.copy_paths()
            self.install_requirements()

            with tempfile.NamedTemporaryFile() as self.temparchive:
                self.archive_function()
                self.ensure_function_role()
                self.create_function()

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

    def ensure_function_role(self):
        role_name = f'lambdapool-role-{self.function_name}'
        role = aws.Role(role_name)
        if not role.exists():
            role.create()
        self.role = role

    def create_function(self):
        print(f'=== Uploading function and dependencies ===')

        with open(self.archive, 'rb') as f:
            archive_data = f.read()

        aws.create_function(self.function_name, archive_data, self.role.get_arn())

        print(f'=== Function {self.function_name} uploaded along with all dependencies ===')
