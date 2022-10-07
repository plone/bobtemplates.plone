# -*- coding: utf-8 -*-

import os

from mrbob.configurator import Configurator

from bobtemplates.plone import base, upgrade_step

from .base import init_package_base_structure


def test_pre_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)
    target_path = os.path.join(package_path, "profiles/default")

    template = """<?xml version='1.0' encoding='UTF-8'?>
<metadata>
  <version>1004</version>
  <dependencies>
    <dependency>profile-plone.app.dexterity:default</dependency>
  </dependencies>
</metadata>
"""
    with open(os.path.join(target_path, "metadata.xml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:upgrade_step",
        target_directory=package_path,
        variables={
            "package_folder": package_path,
            "upgrade_step_title": "Add cool index and reindex it",
            "upgrade_step_description": "We add an index and reindex it with existing content.",
        },
    )
    assert configurator
    upgrade_step.pre_renderer(configurator)
    assert configurator.variables["upgrade_step_source_version"] == 1004
    assert configurator.variables["upgrade_step_dest_version"] == 1005
    assert configurator.variables["upgrade_step_id"] == "1005"


def test_post_renderer(tmpdir):
    target_path = tmpdir.strpath + "/collective.todo"
    package_path = target_path + "/src/collective/todo"
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

    template = """
[main]
version=5.1
"""
    with open(os.path.join(target_path + "/bobtemplate.cfg"), "w") as f:
        f.write(template)

    template = """
    dummy
    '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + "/setup.py"), "w") as f:
        f.write(template)

    template = """
    <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone">

    <!-- -*- extra stuff goes here -*- -->

    </configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:upgrade_step",
        target_directory=package_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "plone.version": "5.1",
            "upgrade_step_title": "Add cool index and reindex it",
            "upgrade_step_description": "We add an index and reindex it with existing content.",
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()


def test_read_source_version(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)
    target_path = os.path.join(package_path, "profiles/default")

    template = """<?xml version='1.0' encoding='UTF-8'?>
<metadata>
  <version>1004</version>
  <dependencies>
    <dependency>profile-plone.app.dexterity:default</dependency>
  </dependencies>
</metadata>
"""
    with open(os.path.join(target_path, "metadata.xml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:upgrade_step",
        target_directory=package_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "plone.version": "5.1",
            "package_folder": package_path,
            "upgrade_step_title": "Add cool index and reindex it",
            "upgrade_step_description": "We add an index and reindex it with existing content.",
        },
    )
    assert configurator
    assert upgrade_step._read_source_version(configurator) == 1004


def test_write_dest_version(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)
    target_path = os.path.join(package_path, "profiles/default")

    template = """<?xml version='1.0' encoding='UTF-8'?>
<metadata>
  <version>1004</version>
  <dependencies>
    <dependency>profile-plone.app.dexterity:default</dependency>
  </dependencies>
</metadata>
"""
    with open(os.path.join(target_path, "metadata.xml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:upgrade_step",
        target_directory=package_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "plone.version": "5.1",
            "package_folder": package_path,
            "upgrade_step_title": "Add cool index and reindex it",
            "upgrade_step_dest_version": 1005,
            "upgrade_step_description": "We add an index and reindex it with existing content.",
        },
    )
    assert configurator
    upgrade_step._write_dest_version(configurator)
    assert upgrade_step._read_source_version(configurator) == 1005
