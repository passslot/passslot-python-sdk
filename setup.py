import sys
from passslot import __version__
from setuptools import setup

# To install the passslot-python-sdk library, open a Terminal shell, then run this
# file by typing:
#
# python setup.py install
#
# You need to have the setuptools module installed. Try reading the setuptools
# documentation: http://pypi.python.org/pypi/setuptools

with open('README.md') as f:
    readme = f.read()
with open('LICENSE.txt') as f:
    license = f.read()
    
    
install_requires = ['requests >= 2.1']
if sys.version_info < (3, 2):
    # This is required for SNI support in python < 3.2
    install_requires.append('pyOpenSSL')
    install_requires.append('ndg-httpsclient')
    install_requires.append('pyasn1')
    
setup(
    name = "passslot",
    version = __version__,
    description = "PassSlot Python SDK",
    author = "PassSlot",
    author_email = "dev@passslot.com",
    url = "http://github.com/passslot/passslot-python-sdk/",
    py_modules = ['passslot'],
    keywords = ["passslot","passbook"],
    install_requires = install_requires,
    license=license,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
        ],
    long_description = readme
 )