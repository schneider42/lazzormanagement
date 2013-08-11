import sys
import subprocess

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='lazzormanagement',
    version='1.0.0',
    description='Tools to manage a lazzor',
    author='Tobias Schneider',
    author_email='schneider@xtort.eu',
    url='https://github.com/schneider42/lazzormanagement',
    packages=['lazzormanagement'],
    long_description=open('README.md').read(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or ",
        "later (GPLv3+)",
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='lasercuter laser cutter lazzor',
    license='GPLv3+',
)
