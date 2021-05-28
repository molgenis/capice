#!/usr/bin/env python3

from setuptools import setup
from capice import __author__, __program__, __version__, __license__

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=__program__,
    version=__version__,
    packages=['src', 'src.main', 'src.main.python', 'src.main.python.core', 'src.main.python.resources',
              'src.main.python.resources.errors', 'src.main.python.resources.models',
              'src.main.python.resources.parsers', 'src.main.python.resources.checkers',
              'src.main.python.resources.imputers', 'src.main.python.resources.utilities',
              'src.main.python.resources.data_files', 'src.main.python.resources.data_files.imputing',
              'src.main.python.resources.data_files.json_data', 'src.main.python.resources.preprocessors'],
    url='https://capice.molgeniscloud.org/',
    license=__license__,
    author=__author__,
    author_email='molgenis-support@umcg.nl',
    description='Consequence Agnostic Pathogenicity Interpretation of Clinical Exoma variations. '
                'State of the art machine learning to predict SNVs and InDels pathogenicity.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: {}'.format(__license__),
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy==1.20.2',
        'pandas==1.2.4',
        'scipy==1.6.2',
        'scikit-learn==0.24.2',
        'xgboost==0.90'
    ],
    entry_points={
        'console_scripts': [
            'capice = capice:main'
        ]
    }

)
