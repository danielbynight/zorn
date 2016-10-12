import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'zorn',
    version = '0.0.1',
    author = 'Daniel Matias Ferrer',
    author_email = 'controlledflame@gmail.com',
    description = 'A static website generator.',
    license = "MIT",
    keywords = 'static website generator',
    url = 'http://controlledflame.com',
    packages=['zorn', 'tests'],
    long_description=read('README.md'),
    classifiers=[],
)