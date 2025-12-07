import os


PYPROJECTTOML_TEMPLATE = """[project]
name = "collective.checklist"
dynamic = ["version"]
description = "A new addon for Plone"
readme = "README.md"
license = "GPL-2.0-only"
requires-python = ">=3.10"
authors = [
    { name = "Plone Community", email = "collective@plone.org" },
]
keywords = [
    "CMS",
    "Plone",
    "Python",
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Framework :: Plone","Framework :: Plone :: 6.0","Framework :: Plone :: 6.1",
    "Framework :: Plone :: Addon",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    "Products.CMFPlone",
    "plone.api",
    "plone.restapi",
    "plone.volto",

]

[project.optional-dependencies]
test = [
    "horse-with-no-namespace",
    "plone.app.testing",
    "plone.restapi[test]",
    "pytest",
    "pytest-cov",
    "pytest-plone>=0.5.0",
]
release = [
    "zest.releaser[recommended]",
    "zestreleaser.towncrier",
    "zest.pocompile",
]

[project.urls]
Homepage = "https://github.com/collective/collective.checklist"
PyPI = "https://pypi.org/project/collective.checklist"
Source = "https://github.com/collective/collective.checklist"
Tracker = "https://github.com/collective/collective.checklist/issues"


[project.entry-points."plone.autoinclude.plugin"]
target = "plone"

[tool.uv]
managed = false

[tool.hatch.version]
path = "src/collective/checklist/__init__.py"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
strict-naming = true

[tool.hatch.build.targets.sdist]
exclude = [
  "/.github",
]

[tool.hatch.build.targets.wheel]
packages = ["src/collective"]

[tool.towncrier]
directory = "news/"
filename = "CHANGELOG.md"
start_string = "<!-- towncrier release notes start -->"
title_format = "## {version} ({project_date})"
template = "news/.changelog_template.jinja"
issue_format = "[#{issue}](https://github.com/collective/collective.checklist/issues/{issue})"
underlines = ["", "", ""]

[[tool.towncrier.type]]
directory = "breaking"
name = "Breaking changes:"
showcontent = true

[[tool.towncrier.type]]
directory = "feature"
name = "New features:"
showcontent = true

[[tool.towncrier.type]]
directory = "bugfix"
name = "Bug fixes:"
showcontent = true

[[tool.towncrier.type]]
directory = "internal"
name = "Internal:"
showcontent = true

[[tool.towncrier.type]]
directory = "documentation"
name = "Documentation:"
showcontent = true

[[tool.towncrier.type]]
directory = "tests"
name = "Tests"
showcontent = true

[tool.ruff]
target-version = "py310"
line-length = 88
fix = true
lint.select = [
    # flake8-2020
    "YTT",
    # flake8-bandit
    "S",
    # flake8-bugbear
    "B",
    # flake8-builtins
    "A",
    # flake8-comprehensions
    "C4",
    # flake8-debugger
    "T10",
    # flake8-simplify
    "SIM",
    # mccabe
    "C90",
    # pycodestyle
    "E", "W",
    # pyflakes
    "F",
    # pygrep-hooks
    "PGH",
    # pyupgrade
    "UP",
    # ruff
    "RUF",
]
lint.ignore = [
    # DoNotAssignLambda
    "E731",
]

[tool.ruff.lint.isort]
case-sensitive = false
no-sections = true
force-single-line = true
from-first = true
lines-after-imports = 2
lines-between-types = 1
order-by-type = false

[tool.ruff.format]
preview = true

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["E501", "RUF001", "S101"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
source_pkgs = ["collective.checklist", "tests"]
branch = true
parallel = true
omit = [
  "src/collective/checklist/locales/*.py",
]

[tool.zest-releaser]
python-file-with-version = "src/collective/checklist/__init__.py"
"""

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

    template = PYPROJECTTOML_TEMPLATE

    with open(os.path.join(package_root + "/pyproject.toml"), "w") as f:
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
