# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


version = "6.2.5"


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="bobtemplates.plone",
    version=version,
    description="Templates for Plone projects.",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Framework :: Plone",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="web plone zope skeleton project",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/bobtemplates.plone/",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/bobtemplates.plone",
        "Documentation": "https://bobtemplatesplone.readthedocs.io/en/latest/",
        "Source": "https://github.com/plone/bobtemplates.plone/",
        "Tracker": "https://github.com/plone/bobtemplates.plone/issues",
    },
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["bobtemplates"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        "mr.bob",
        "lxml",
        "case-conversion",
        "colorama",
        "tox",
        "isort",
        "black",
    ],
    setup_requires=[],
    tests_require=[],
    extras_require={},
    entry_points={
        "mrbob_templates": [
            "plone_addon = bobtemplates.plone.bobregistry:plone_addon",
            "plone_behavior = bobtemplates.plone.bobregistry:plone_behavior",
            "plone_buildout = bobtemplates.plone.bobregistry:plone_buildout",
            "plone_content_type = bobtemplates.plone.bobregistry:plone_content_type",
            "plone_indexer = bobtemplates.plone.bobregistry:plone_indexer",
            "plone_mockup_pattern = bobtemplates.plone.bobregistry:plone_mockup_pattern",
            "plone_portlet = bobtemplates.plone.bobregistry:plone_portlet",
            "plone_restapi_service = bobtemplates.plone.bobregistry:plone_restapi_service",  # NOQA E501
            "plone_svelte_app = bobtemplates.plone.bobregistry:plone_svelte_app",
            "plone_subscriber = bobtemplates.plone.bobregistry:plone_subscriber",
            "plone_theme = bobtemplates.plone.bobregistry:plone_theme",
            "plone_theme_barceloneta = bobtemplates.plone.bobregistry:plone_theme_barceloneta",  # NOQA E501
            "plone_theme_basic = bobtemplates.plone.bobregistry:plone_theme_basic",  # NOQA E501
            "plone_upgrade_step = bobtemplates.plone.bobregistry:plone_upgrade_step",
            "plone_view = bobtemplates.plone.bobregistry:plone_view",
            "plone_viewlet = bobtemplates.plone.bobregistry:plone_viewlet",
            "plone_vocabulary = bobtemplates.plone.bobregistry:plone_vocabulary",
            "plone_controlpanel = bobtemplates.plone.bobregistry:plone_controlpanel",
            "plone_form = bobtemplates.plone.bobregistry:plone_form",
        ]
    },
)
