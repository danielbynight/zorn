import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='zorn',
    version='1.0.0',
    author='Daniel Matias Ferrer',
    author_email='controlledflame@gmail.com',
    description='A light static website generator.',
    license='MIT',
    keywords='static website generator',
    url='http://controlledflame.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'markdown',
        'Jinja2'
    ],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: JavaScript',
    ],
)
