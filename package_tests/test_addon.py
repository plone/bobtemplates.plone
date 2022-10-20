# -*- coding: utf-8 -*-

from bobtemplates.plone import addon
from bobtemplates.plone import base
from mrbob.configurator import Configurator

import os


def test_pre_render(tmpdir):
    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=tmpdir.strpath + "collective.foo.bar",
        variables={
            "package.dexterity_type_name": "Task",
        },
    )
    addon.pre_render(configurator)


def test_cleanup_package(tmpdir):
    target_path = tmpdir.strpath + "/collective.foo.bar"
    package_path = target_path + "/src/collective/foo/bar"
    profiles_path = package_path + "/profiles/default"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profiles_path)
    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + "/metadata.xml"), "w") as f:
        f.write(template)

    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=target_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "package.nested": True,
            "package.namespace": "collective",
            "package.namespace2": "foo",
            "package.name": "bar",
            "year": 1970,
            "package.git.init": True,
            "package.description": "Test",
            "author.name": "The Plone Collective",
            "author.email": "collective@plone.org",
            "author.github.user": "collective",
            "plone.version": "5.1",
            "python.version": "python2.7",
            "plone.is_plone5": True,
            "vscode_support": True,
        },
    )
    assert configurator
    base.set_global_vars(configurator)
    configurator.render()


def test_no_namespace(tmpdir):
    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=tmpdir.strpath + "mypackage",
        variables={},
    )
    addon.pre_render(configurator)
    name = os.path.split(tmpdir.strpath + "mypackage")[-1]
    assert configurator.variables["package.dottedname"] == name
    assert configurator.variables["package.distributionname"] == name


def test_with_dash(tmpdir):
    # no namespace
    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=tmpdir.strpath + "my-package",
        variables={},
    )
    addon.pre_render(configurator)
    package_name = os.path.split(tmpdir.strpath + "my_package")[-1]
    distribution_name = os.path.split(tmpdir.strpath + "my-package")[-1]
    assert configurator.variables["package.dottedname"] == package_name
    assert configurator.variables["package.distributionname"] == distribution_name

    # with namespace
    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=tmpdir.strpath + "my-namespace.my-package",
        variables={},
    )
    addon.pre_render(configurator)
    package_name = os.path.split(tmpdir.strpath + "my_namespace.my_package")[-1]
    distribution_name = os.path.split(tmpdir.strpath + "my-namespace.my-package")[-1]
    assert configurator.variables["package.dottedname"] == package_name
    assert configurator.variables["package.distributionname"] == distribution_name
