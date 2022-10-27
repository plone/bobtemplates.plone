# -*- coding: utf-8 -*-

"""Test form generation."""

from .base import init_package_base_structure
from bobtemplates.plone import base
from bobtemplates.plone import form
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import os


def test_get_form_name():
    question = Question(name="form_name", question="", default=None)
    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"form_python_class_name": "FancyDemoForm"},
    )
    form.get_form_name_from_python_class(configurator, question)
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
        target_directory=target_path,
        bobconfig={"non_interactive": True},
        variables={
            "form_python_file_name": "py_form",
            "form_python_class_name": "MyForm",
            "form_register_for": "Folder",
            "form_name": "py-form",
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
    permission="cmf.ManagePortal"
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
            "form_name": "my-new-form",
            "form_python_class_name": "New_Form",
            "form_register_for": "plone.app.contenttypes.interfaces.IFolder",
            "plone.version": "6.0",
        },
    )
    form.prepare_renderer(configurator)

    assert configurator.variables["form_name"] == "my-new-form"
    assert configurator.variables["form_python_class_name"] == "NewForm"
    assert configurator.variables["form_python_file_name"] == "new_form"

    configurator = Configurator(
        template="bobtemplates.plone:form",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "form_name": "my-new-form",
            "form_python_class_name": "MyNewForm",
            "form_register_for": "*",
            "plone.version": "5.1",
        },
    )

    form.prepare_renderer(configurator)

    assert configurator.variables["form_name"] == "my-new-form"
    assert (
        configurator.variables["form_python_file_name"]
        == configurator.variables["form_name_normalized"]
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
            "form_name": "my-new-form",
            "form_python_class_name": "NewForm",
            "form_register_for": "*",
            "plone.version": "5.1",
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()  # pre/render/post
