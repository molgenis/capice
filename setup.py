#!/usr/bin/env python3

from setuptools import setup, find_packages
from src.main.python.__version__ import __version__

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='capice',
    version=__version__,
    packages=find_packages('src', exclude=['test']),
    package_dir={"": "src"},
    url='https://capice.molgeniscloud.org/',
    license='LGPL-3.0',
    author='Shuang Li, Robert Sietsma and Molgenis',
    author_email='molgenis-support@umcg.nl',
    description='Consequence Agnostic Pathogenicity Interpretation of '
                'Clinical Exoma variations. State of the art machine learning '
                'to predict SNVs and InDels pathogenicity.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: LGPL-3.0',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.7.1',
    install_requires=[
        'numpy==1.21.3',
        'pandas==1.3.5',
        'scipy==1.7.3',
        'scikit-learn==1.0.2',
        'xgboost==1.4.2'
    ],
    extras_require={
        'testing': ['pytest']
    },
    entry_points={
        'console_scripts': [
            'capice = capice:main'
        ]
    }

)
