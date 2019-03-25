# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


version = '4.0.2'


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='bobtemplates.plone',
    version=version,
    description='Templates for Plone projects.',
    long_description=long_description,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
    keywords='web plone zope skeleton project',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/plone/bobtemplates.plone',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['bobtemplates'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'mr.bob',
        'lxml',
        'case-conversion',
        'colorama',
    ],
    setup_requires=[],
    tests_require=[],
    extras_require={},
    entry_points={
        'mrbob_templates': [
            'plone_addon = bobtemplates.plone.bobregistry:plone_addon',
            'plone_buildout = bobtemplates.plone.bobregistry:plone_buildout',  # NOQA E501
            'plone_theme_package = bobtemplates.plone.bobregistry:plone_theme_package',  # NOQA E501
            'plone_content_type = bobtemplates.plone.bobregistry:plone_content_type',  # NOQA E501
            'plone_view = bobtemplates.plone.bobregistry:plone_view',
            'plone_viewlet = bobtemplates.plone.bobregistry:plone_viewlet',
            'plone_portlet = bobtemplates.plone.bobregistry:plone_portlet',
            'plone_theme = bobtemplates.plone.bobregistry:plone_theme',
            'plone_theme_barceloneta = bobtemplates.plone.bobregistry:plone_theme_barceloneta',  # NOQA E501
            'plone_vocabulary = bobtemplates.plone.bobregistry:plone_vocabulary',  # NOQA E501
            'plone_behavior = bobtemplates.plone.bobregistry:plone_behavior',  # NOQA E501
            'plone_restapi_service = bobtemplates.plone.bobregistry:plone_restapi_service',  # NOQA E501
        ],
    },
)
