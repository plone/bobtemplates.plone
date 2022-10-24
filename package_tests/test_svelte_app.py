# -*- coding: utf-8 -*-

from .base import init_package_base_structure
from bobtemplates.plone import base
from bobtemplates.plone import svelte_app
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import os
import pytest


def test_prep_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    init_package_base_structure(package_root)
    configurator = Configurator(
        template="bobtemplates.plone:svelte_app",
        target_directory=package_root,
        variables={
            "svelte_app_name": "my-cool-svelte-app",
        },
    )
    svelte_app.pre_renderer(configurator)


def test_check_name(tmpdir):
    target_path = tmpdir.strpath + "/collective.todo"
    question = Question(
        name="svelte_app_name", question="Name of your Svelte app", default=None
    )
    configurator = Configurator(
        template="bobtemplates.plone:svelte_app",
        target_directory=target_path,
        bobconfig={"non_interactive": True},
    )
    with pytest.raises(ValidationError):
        svelte_app.check_name(configurator, question, "My-Svelteapp")
    with pytest.raises(ValidationError):
        svelte_app.check_name(configurator, question, "MySvelteApp")
    with pytest.raises(ValidationError):
        svelte_app.check_name(configurator, question, "mysvelteapp")
    with pytest.raises(ValidationError):
        svelte_app.check_name(configurator, question, "my_svelteapp")
    with pytest.raises(ValidationError):
        svelte_app.check_name(configurator, question, "my_svelte_app")
    assert svelte_app.check_name(configurator, question, "my-app") == "my-app"
    assert (
        svelte_app.check_name(configurator, question, "my-svelte-app")
        == "my-svelte-app"
    )
    assert (
        svelte_app.check_name(configurator, question, "my-cool-svelte-app")
        == "my-cool-svelte-app"
    )
    assert (
        svelte_app.check_name(configurator, question, "my-cool-svelte-app-one")
        == "my-cool-svelte-app-one"
    )


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
        template="bobtemplates.plone:svelte_app",
        target_directory=target_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "plone.version": "5.2",
            "svelte_app_name": "my-cool-svelte-app",
            "svelte_app_custom_element": True,
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    svelte_app.pre_renderer(configurator)
    configurator.render()
    svelte_app.post_renderer(configurator)
    # FIXME: check if the setting and files are in place
