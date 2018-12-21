#!/usr/bin/env python
from setuptools import setup, find_packages
from kubecli import VERSION

# Setup
setup(
    name='kubecli',
    version=VERSION,
    description='Kubernetes testing library',
    long_description='Wrapper on Kubernetes client library for testing',
    author='sampath',
    keywords='',
    packages=find_packages(exclude=('docs', 'tests', 'env')),
    include_package_data=True,
#    install_requires=[
#		'kubernetes-client'
#   ],
    extras_require={
    'dev': [],
    'docs': [],
    'testing': [],
    },
    classifiers=[],
    )
