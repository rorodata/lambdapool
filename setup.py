import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyminion",
    version="0.2.1",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/palnabarun/lambda-pool",
    author="Nabarun Pal",
    author_email="pal.nabarun95@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["minion"],
    include_package_data=True,
    install_requires=["boto3"],
)
