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
    install_requires=[
        'nose',
        'sphinx',
        'requests==2.11.1',
        'vcrpy==1.10.3',
        'pytest==3.0.3',
        'bunch'
    ],
    packages=find_packages(exclude=('tests', 'docs'))
)

