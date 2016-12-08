import sys
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import dmp

setup(
    name='dmp',
    version=dmp.__version__,
    description='MuG DMP API',
    url='http://www.multiscalegenomics.eu',
    download_url='https://github.com/Multiscale-Genomics/mg-dm-api',
    author=dmp.__author__,
    author_email='mcdowall@ebi.ac.uk',
    license=dmp.__license__,
    #packages=find_packages(),
    include_package_data=True,
    install_requires = [
        'pymongo>=3.3', 'mongomock>=3.7'
    ]
)
