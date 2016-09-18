from setuptools import setup, find_packages

from codecs import open

from os import path 

here = path.abspath(path.dirname(__file__))
long_desc = ''
with open(path.join(here,'README.md'), encoding='utf-8') as f:
    long_desc = f.read()
setup(
      name='Pynance',
      version='0.2.3',
      description="Financial Utilities Project for python",
      long_description=long_desc,
      url="https://github.com/rcoverick/Pynance",
      author="Ryan Coverick",
      author_email="rcoverick@gmail.com",
      license="GPL-3.0",
      
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers, Stock Traders, and Finance Enthusiasts',
        'Topic :: Finance :: Tools',
        'License :: OSI Approved :: GNU General Public License 3.0',
        'Programming Language :: Python :: 3.5'
        ],
      
      keywords='finance web scrape analysis budget stock market trading budgeting',
      packages=find_packages(),
      install_requires=['lxml','requests','beautifulsoup4'],
      
      )
