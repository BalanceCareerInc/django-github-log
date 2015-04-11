#!/usr/bin/env python

from setuptools import setup, find_packages
from github_log import VERSION

github_url = 'https://github.com/BalanceCareerInc/django-github-log/'

setup(
    name='django-github-log',
    version=VERSION,
    description='Django log handler to create issue on github automatically',
    long_description=open('README.rst').read(),
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
