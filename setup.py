from tabnanny import check
from setuptools import setup, find_packages

setup(
    name='Ckeck',
    version='0.0.1',
    description='This packege help to check versions',
    packages=find_packages(exclude=('tests')),
    entry_points={
        'console_scripts': [
            'check-file = bin.check:main',
        ],
    },

    
)
