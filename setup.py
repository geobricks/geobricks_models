from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksModels',
    version='0.0.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks Models library.',
    install_requires=[
        # 'watchdog',
        # 'flask',
        # 'flask-cors',
        # 'requests'
    ],
    url='http://pypi.python.org/pypi/GeobricksModels/',
    keywords=['gis']
)
