#!/usr/bin/env python

from setuptools import setup


setup(
    name='certificat-covid-eu',
    version='0.0.1',
    author='Telmo Menezes',
    author_email='telmo@telmomenezes.net',
    description='Scraper for EU public consultation.',
    python_requires='>=3.6',
    install_requires=[
        'selenium',
        'beautifulsoup4'
    ]
)
