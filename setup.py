#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages
from src.molgenis.capice.__version__ import __version__

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='capice',
    version=__version__,
    packages=find_namespace_packages('src', exclude=['tests', 'scripts']),
    package_dir={"": "src"},
    url='https://capice.molgeniscloud.org/',
    license='LGPL-3.0',
    author='Shuang Li, Robert Sietsma and Molgenis',
    author_email='molgenis-support@umcg.nl',
    description='Consequence Agnostic Pathogenicity Interpretation of '
                'Clinical Exoma variations. State of the art machine learning '
                'to predict SNVs and InDels pathogenicity.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy==1.21.0',
        'pandas==1.2.4',
        'scipy==1.6.2',
        'scikit-learn==0.24.2',
        'xgboost==1.4.2'
    ],
    entry_points={
        'console_scripts': [
            'capice = molgenis.capice.capice:main'
        ]
    }

)
