#!/usr/bin/env python

from setuptools import setup, find_packages


version = '0.0.12'

setup(
    name='harry',
    version=version,
    description='harry converts HTTP Archives (.har) into JMeter test plans (.jmx).',
    author='Zach Munro-Cape',
    author_email='zach.munrocape@gmail.com',
    license='apache',
    keywords=['jmeter', 'http archive', 'har2jmx', 'command line', 'cli'],
    url='https://github.com/munrocape/harry',
    download_url='https://github.com/peterldowns/mypackage/tarball/'+version,
    packages=find_packages(),
    package_data={
            'harry': ['harpy/harpy/*']
        },
    install_requires=[
        'docopt>=0.6.1',
    ],
    entry_points={
    'console_scripts': [
        'harry=harry.harry:main',
    ],
}
)