#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='docktree',
    version='0.1.0',
    description='Display the tree structure of your Docker images',
    url='https://github.com/cmihai/docktree',
    author='Mihai Ciumeică',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    install_requires=['docker_py>=1.5.0'],
    entry_points={
        'console_scripts': [
            'docktree=docktree:main'
        ]
    }
)
