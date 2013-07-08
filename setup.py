# -*- coding: utf8 -*-

from setuptools import find_packages
from setuptools import setup

version = '0.4'

setup(
    name='bobtemplates.ecreall',
    version=version,
    description="Templates for Ecréall projects.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    keywords='',
    author='Cédric Messiant',
    author_email='cedricmessiant@ecreall.com',
    url='https://github.com/cedricmessiant/bobtemplates.ecreall',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['bobtemplates'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'mr.bob',
    ],
    extras_require={
        'test': [
            'nose',
            'nose-selecttests',
            'scripttest',
            'unittest2',
        ]
    },
    entry_points={},
)
