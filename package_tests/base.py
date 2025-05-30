import os


SETUPPY_TEMPLATE = """
from setuptools import find_packages
from setuptools import setup

long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)

setup(
    name="collective.checklist",
    version="0.1a3.dev0",
    description="Checklist App for Plone",
    long_description=long_description,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Maik Derstappen",
    author_email="md@derico.de",
    url="https://github.com/collective/collective.checklist",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.checklist/",
        "Source": "https://github.com/collective/collective.checklist",
        "Tracker": "https://github.com/collective/collective.checklist/issues",
        # 'Documentation': 'https://collective.checklist.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.app.dexterity",
        "plone.schema",
        "plone.app.z3cform>=4.4.1",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
)
"""


def init_package_base_structure(package_root):
    """creates initial folder and file structure for packages tests.
    expects: package_root
    returns: package_path
    """
    package_name = package_root.split("/")[-1]
    namespace_parts = package_name.split(".")
    package_namespace_path = "/".join(namespace_parts)
    package_path = os.path.join(package_root, "src/" + package_namespace_path)
    profiles_path = os.path.join(package_path, "profiles/default")
    svelte_apps_path = os.path.join(package_path, "svelte_apps")
    theme_path = os.path.join(package_path, "theme")
    os.makedirs(package_root)
    os.makedirs(package_path)
    os.makedirs(profiles_path)
    os.makedirs(svelte_apps_path)
    os.makedirs(theme_path)
    template = """
[main]
version=5.1
"""
    with open(os.path.join(package_root + "/bobtemplate.cfg"), "w") as f:
        f.write(template)

    template = SETUPPY_TEMPLATE

    with open(os.path.join(package_root + "/setup.py"), "w") as f:
        f.write(template)

    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

  <i18n:registerTranslations directory="locales" />

  <!--
    Be careful if you use general includeDependencies, it can have sideffects!
    Better import explicite packages or configurations ;)
  -->
  <!--<includeDependencies package="." />-->

  <!-- -*- extra stuff goes here -*- -->

</configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)

    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + "/metadata.xml"), "w") as f:
        f.write(template)

    return package_path
