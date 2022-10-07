# -*- coding: utf-8 -*-

import os

from mrbob.configurator import Configurator

from bobtemplates.plone import base, vocabulary


def test_prepare_renderer():
    configurator = Configurator(
        template="bobtemplates.plone:vocabulary",
        target_directory=".",
        variables={
            "vocabulary_name": "ExampleVocabulary",
        },
    )
    vocabulary.prepare_renderer(configurator)


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
        template="bobtemplates.plone:vocabulary",
        target_directory=package_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "plone.version": "5.1",
            "vocabulary_name": "AvailableTasks",
            "vocabulary_description": "Bla",
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    vocabulary.prepare_renderer(configurator)
    configurator.render()
    vocabulary.post_renderer(configurator)
