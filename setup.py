import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lambda-pool",
    version="0.4.1",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rorodata/lambda-pool",
    author="Nabarun Pal",
    author_email="pal.nabarun95@gmail.com",
    packages=["lambdapool"],
    include_package_data=True,
    install_requires=["boto3"],
)
