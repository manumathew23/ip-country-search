# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Application name:
    name="ip_country_search",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="Manu Mathew",
    author_email="manumatew@gmail.com",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/manumathew23/ip-country-search",

    # license="LICENSE.txt",
    description="A python utility for searching country name for ipaddress",

    long_description_content_type='text/markdown', 

    # Dependent packages (distributions)
    install_requires=[
        "certifi",
        "chardet",
        "idna",
        "numpy",
        "Pillow",
        "requests",
        "six",
        "urllib3"
    ],
)