#!/usr/bin/env python3
import io
from glob import glob
from os.path import basename, splitext, exists
from setuptools import find_packages, setup

PROJECT_NAME = 'evtxtool'
VERSION = '0.0.2'
DESCRIPTION = 'Convert an evtx file (GitHub.com/omerbenamram/evtx) to json.'
EMAIL = 'spyrr83@gmail.com'

REQUIREMENTS_FILENAME='./requirements.txt'
contents = ''
if exists(REQUIREMENTS_FILENAME):
    with open(REQUIREMENTS_FILENAME, 'r') as f:
        contents = f.read().split('\n')
REQUIREMENTS = list(filter(None, contents))

ENTRYPOINTS = {
    'console_scripts': [
        f'{PROJECT_NAME} = evtxtool:main', 
    ],
}
DATAFILES=[]
KEYWORDS = ['evtx', 'json', 'csv', 'convert']
#DATAFILES = [('data', ['src/data/template.xlsm',]),]

setup(
    name=PROJECT_NAME,
    version='0.0.1',
    description=DESCRIPTION,
    author='Hosub Lee',
    author_email=EMAIL,
    install_requires=REQUIREMENTS,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    keywords=KEYWORDS,
    python_requires='>=3.6',
    data_files=DATAFILES,
    entry_points=ENTRYPOINTS,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
