# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='labguru',
    version='0.1.0',
    description='Labguru Python API',
    long_description=readme,
    author='Tran Xuan Tu',
    author_email='xtutran@gmail.com',
    url='https://github.com/BioData/LabguruPython',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

