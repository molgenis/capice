from setuptools import setup

setup(
    name='capice',
    version='2.0',
    packages=['src', 'src.main', 'src.main.python', 'src.main.python.core', 'src.main.python.resources',
              'src.main.python.resources.errors', 'src.main.python.resources.models',
              'src.main.python.resources.parsers', 'src.main.python.resources.checkers',
              'src.main.python.resources.imputers', 'src.main.python.resources.utilities',
              'src.main.python.resources.data_files', 'src.main.python.resources.data_files.imputing',
              'src.main.python.resources.preprocessors'],
    url='https://capice.molgeniscloud.org/',
    license='LGPL-3.0',
    author='Shuang Li, Robert Sietsma and Molgenis',
    author_email='molgenis-support@umcg.nl',
    description='Consequence Agnostic Pathogenicity Interpretation of Clinical Exoma variations. '
                'State of the art machine learning to predict SNVs and InDels pathogenicity.',
    long_description='file: README.md',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: LGPL-3.0',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    python_requires='>=3.6,<=3.8',
    install_requires=[
        'numpy==1.18.1',
        'pandas==1.0.2',
        'scikit-learn==0.23.1',
        'xgboost==1.1.1'
    ]
)
