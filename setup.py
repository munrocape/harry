#!/usr/bin/env python

from setuptools import setup, find_packages


version = '0.0.1'

setup(
    name='harry',
    version=version,
    description='harry converts HTTP Archives (.har) into JMeter test plans (.jmx).',
    long_description=open('README.rst').read(),
    author='Zach Munro-Cape',
    author_email='zach.munrocape@gmail.com',
    license='MIT',
    keywords=['jmeter', 'http archive', 'har2jmx', 'command line', 'cli'],
    url='http://github.com/munrocape/harry',
    packages=find_packages(),
    install_requires=[
        'docopt>=0.6.1',
    ],
    entry_points={
        'console_scripts': [
            'harry=harry.harry:main'
        ],
    }
)