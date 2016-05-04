#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='docktree',
    version='0.3.1',
    description='Display the local Docker image layers as a tree',
    long_description=long_description,
    url='https://github.com/cmihai/docktree',
    author='Mihai Ciumeică',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4 ',
    ],
    packages=find_packages(),
    install_requires=['docker_py>=1.5.0'],
    entry_points={
        'console_scripts': [
            'docktree=docktree:main'
        ]
    }
)
