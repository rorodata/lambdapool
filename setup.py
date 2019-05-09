import os
import pathlib
from setuptools import setup

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

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lambda-pool",
    version=get_version(),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rorodata/lambda-pool",
    author="Nabarun Pal",
    author_email="pal.nabarun95@gmail.com",
    packages=["lambdapool"],
    include_package_data=True,
    install_requires=["boto3", "click", "tabulate"],
    entry_points='''
        [console_scripts]
        lambdapool=lambdapool.cli:cli
    '''
)
