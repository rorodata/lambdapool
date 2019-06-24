import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="lambda-pool",
    version="0.9.5",
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
