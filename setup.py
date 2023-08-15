from setuptools import setup, find_packages

# Package metadata
NAME = 'pearley'
VERSION = '0.1.0'
DESCRIPTION = 'Basic Python Earley Parser'
AUTHOR = 'Paul Arelt'
EMAIL = 'your@email.com'
URL = 'https://github.com/your_username/your_package_repo'
LICENSE = 'Apache'

REQUIRES = [
    'pytest==6.2.4'
]

# Package classifiers (See: https://pypi.org/classifiers/)
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

# Read the README file for long description
with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Setup configuration
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    install_requires=REQUIRES,
    classifiers=CLASSIFIERS,
    python_requires='>=3.7',
)
