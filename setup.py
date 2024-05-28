# /MyUtils/setup.py

from setuptools import setup, find_packages

setup(
    name='MyUtils',
    version='0.2.0',  # Update this version number as needed
    packages=find_packages(),
    install_requires=[
        'setuptools~=57.4.0',
        'requests~=2.31.0',
        'openai~=1.23.6',
        'ifcopenshell~=0.7.0.231218',
        'neo4j~=5.20.0',
        'numpy~=1.26.4'
    ],
    description='A collection of utility functions for multiple projects',
    author='Elia Wäfler',
    author_email='elia.waefler@gmail.com',
    url='https://github.com/eliawaefler/MyUtils'
)
