import os
import pathlib
from setuptools import setup, find_packages

def get_version():
    """Returns the package version taken from version.py.
    """
    root = os.path.dirname(__file__)
    version_path = os.path.join(root, "lambdapool/version.py")
    with open(version_path) as f:
        code = f.read()
        env = {}
        exec(code, env, env)
        return env['__version__']

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="lambda-pool",
    version=get_version(),
    author='rorodata',
    author_email='rorodata.team@gmail.com',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rorodata/lambda-pool",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "boto3",
        "click",
        "tabulate",
        "cloudpickle"
    ],
    entry_points='''
        [console_scripts]
        lambdapool=lambdapool.cli:cli
    '''
)
