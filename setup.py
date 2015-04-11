#!/usr/bin/env python

from setuptools import setup, find_packages
from github_log import VERSION

github_url = 'https://github.com/BalanceCareerInc/django-github-log/'

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='django-github-log',
    version=VERSION,
    description='Django log handler to create issue on github automatically',
    long_description=read_md('README.md'),
    author='Seungyeon Joshua Kim(Acuros)',
    author_email='acuroskr' '@' 'gmail.com',
    license='MIT License',

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'celery',
        'pygithub3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
