# -*- coding: utf-8 -*-

"""Test view generation."""

import os

import pytest
from mrbob.bobexceptions import SkipQuestion, ValidationError
from mrbob.configurator import Configurator, Question

from bobtemplates.plone import base, form

from .base import init_package_base_structure


def test_get_view_name():
    question = Question(name="view_name", question="", default=None)
    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class_name": "FancyDemoForm"},
    )
    form.get_view_name_from_python_class(configurator, question)
    assert question.default == "fancy-demo-form"


def test_update_forms_configure_zcml(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    forms_path = package_path + "/forms/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(forms_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

</configure>
"""
    with open(os.path.join(forms_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "view_python_class_name": "MyForm",
            "view_register_for": "Folder",
            "view_name": "py-form",
            "package_folder": package_path,
            "package.dottedname": "collective.sample",
            "package.browserlayer": "CollectiveSampleLayer",
        },
    )
    form._update_forms_configure_zcml(configurator)

    expected = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

  <browser:page
    name="py-form"
    for="plone.app.contenttypes.interfaces.IFolder"
    class=".py_form.MyForm"
    permission="zope2.View"
    layer="collective.sample.interfaces.ICollectiveSampleLayer"
    />

</configure>
"""
    with open(os.path.join(forms_path + "configure.zcml"), "r") as f:
        content = f.read()
        assert content == expected


def test_update_configure_zcml(tmpdir):
    target_path = tmpdir.strpath + "/collective.demo"
    package_path = target_path + "/src/collective/demo"
    os.makedirs(target_path)
    os.makedirs(package_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.demo">

  <i18n:registerTranslations directory="locales" />

  <!--<includeDependencies package="." />-->

  <include package=".browser" />
  <!-- -*- extra stuff goes here -*- -->

</configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory="collective.demo",
        bobconfig={"non_interactive": True},
        variables={"package_folder": package_path},
    )
    form._update_configure_zcml(configurator)


def test_pre_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class_name": "New_View",
            "view_register_for": "plone.app.contenttypes.interfaces.IFolder",
            "plone.version": "6.0",
        },
    )
    form.prepare_renderer(configurator)

    assert configurator.variables["view_name"] == "my-new-view"
    assert configurator.variables["view_python_class_name"] == "NewView"
    assert configurator.variables["view_python_file_name"] == "new_view"

    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class_name": "MyNewView",
            "view_register_for": "*",
            "plone.version": "5.1",
        },
    )

    form.prepare_renderer(configurator)

    assert configurator.variables["view_name"] == "my-new-view"
    assert (
        configurator.variables["view_python_file_name"]
        == configurator.variables["view_name_normalized"]
    )


def test_post_renderer(tmpdir):
    """Test post rendering."""
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class_name": "NewView",
            "view_register_for": "*",
            "plone.version": "5.1",
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()  # pre/render/post
