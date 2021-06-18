# -*- coding: utf-8 -*-

"""Test view generation."""

import os

import pytest
from mrbob.bobexceptions import SkipQuestion, ValidationError
from mrbob.configurator import Configurator, Question

from bobtemplates.plone import base, view

from .base import init_package_base_structure


def test_get_view_name():
    question = Question(name="view_name", question="", default=None)
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": True, "view_python_class_name": "DemoView"},
    )
    view.get_view_name_from_python_class(configurator, question)
    assert question.default == "demo-view"


def test_get_view_template_name():
    question = Question(name="view_template_name", question="", default=None)
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": True, "view_python_class_name": "DemoView"},
    )
    view.get_view_template_name_from_python_class(configurator, question)
    assert question.default == "demo_view"


def test_python_class_true():
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": True},
    )
    view.check_python_class_answer(configurator, None)


def test_python_class_false():
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": False},
    )
    with pytest.raises(SkipQuestion):
        view.check_python_class_answer(configurator, None)


def test_view_template_true():
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": True, "view_template": True},
    )
    view.check_view_template_answer(configurator, None)


def test_view_template_false():
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": True, "view_template": False},
    )
    with pytest.raises(SkipQuestion):
        view.check_view_template_answer(configurator, None)


def test_view_template_and_python_class_false():
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.foo.bar",
        bobconfig={"non_interactive": True},
        variables={"view_python_class": False, "view_template": False},
    )
    with pytest.raises(ValidationError):
        view.check_view_template_answer(configurator, None)


def test_update_views_configure_zcml(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    views_path = package_path + "/views/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

</configure>
"""
    with open(os.path.join(views_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "view_python_class": True,
            "view_python_class_name": "MyView",
            "view_python_file_name": "py_view",
            "view_name": "py-view",
            "view_template": True,
            "view_template_name": "pt_view",
            "package_folder": package_path,
        },
    )
    view._update_views_configure_zcml(configurator)

    expected = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

  <browser:page
    name="py-view"
    for="Products.CMFCore.interfaces.IFolderish"
    class=".py_view.MyView"
    template="pt_view.pt"
    permission="zope2.View"
    />

</configure>
"""
    with open(os.path.join(views_path + "configure.zcml"), "r") as f:
        content = f.read()
        assert content == expected


def test_update_views_configure_zcml_without_template(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    views_path = package_path + "/views/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

</configure>
"""
    with open(os.path.join(views_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "view_python_class": True,
            "view_python_class_name": "MyView",
            "view_python_file_name": "py_view",
            "view_name": "py-view",
            "view_template": False,
            "package_folder": package_path,
        },
    )
    view._update_views_configure_zcml(configurator)

    expected = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

  <browser:page
    name="py-view"
    for="Products.CMFCore.interfaces.IFolderish"
    class=".py_view.MyView"
    permission="zope2.View"
    />

</configure>
"""
    with open(os.path.join(views_path + "configure.zcml"), "r") as f:
        content = f.read()
        assert content == expected


def test_update_views_configure_zcml_without_python_class(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    views_path = package_path + "/views/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

</configure>
"""
    with open(os.path.join(views_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "view_python_class": False,
            "view_name": "py-view",
            "view_template": True,
            "view_template_name": "pt_view",
            "package_folder": package_path,
        },
    )
    view._update_views_configure_zcml(configurator)

    expected = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

  <browser:page
    name="py-view"
    for="Products.CMFCore.interfaces.IFolderish"
    template="pt_view.pt"
    permission="zope2.View"
    />

</configure>
"""

    with open(os.path.join(views_path + "configure.zcml"), "r") as f:
        content = f.read()
        assert content == expected


def test_delete_unwanted_files_template(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)
    views_path = os.path.join(package_path + "/views/")

    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class": False,
            "view_python_class_name": "NewView",
            "view_template": True,
            "view_template_name": "new_view",
            "plone.version": "5.1",
        },
    )
    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()  # pre/render/post
    # as the post_rederer also calls delete_unwanted_files. we don't need to call here
    python_file_name = configurator.variables.get("view_python_file_name") + ".py"
    template_file_name = configurator.variables.get("view_template_name") + ".pt"
    python_file_path = os.path.join(views_path + python_file_name)
    template_file_path = os.path.join(views_path + template_file_name)
    assert os.path.isfile(template_file_path)
    assert not os.path.isfile(python_file_path)


def test_delete_unwanted_files_python(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)
    views_path = os.path.join(package_path + "/views/")

    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class": True,
            "view_python_class_name": "NewView",
            "view_template": False,
            "view_template_name": "new_view",
            "plone.version": "5.1",
        },
    )
    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()  # pre/render/post
    # as the post_rederer also calls delete_unwanted_files. we don't need to call here
    python_file_name = configurator.variables.get("view_python_file_name") + ".py"
    template_file_name = configurator.variables.get("view_template_name") + ".pt"
    python_file_path = os.path.join(views_path + python_file_name)
    template_file_path = os.path.join(views_path + template_file_name)
    assert not os.path.isfile(template_file_path)
    assert os.path.isfile(python_file_path)


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

</configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory="collective.demo",
        bobconfig={"non_interactive": True},
        variables={"package_folder": package_path},
    )
    view._update_configure_zcml(configurator)


def test_pre_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class": True,
            "view_python_class_name": "New_View",
            "view_base_class": "BrowserView",
            "view_template": True,
            "view_template_name": "new_view",
            "plone.version": "5.1",
        },
    )

    view.prepare_renderer(configurator)

    assert configurator.variables["view_name"] == "my-new-view"
    assert configurator.variables["view_python_class_name"] == "NewView"
    assert configurator.variables["view_python_file_name"] == "new_view"

    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class": False,
            "view_template": False,
            "plone.version": "5.1",
        },
    )

    view.prepare_renderer(configurator)

    assert configurator.variables["view_name"] == "my-new-view"
    assert (
        configurator.variables["view_python_file_name"]
        == configurator.variables["view_name_normalized"]
    )
    assert (
        configurator.variables["view_template_name"]
        == configurator.variables["view_name_normalized"]
    )


def test_post_renderer(tmpdir):
    """Test post rendering."""
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:view",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "view_name": "my-new-view",
            "view_python_class": True,
            "view_python_class_name": "NewView",
            "view_base_class": "BrowserView",
            "view_template": True,
            "view_template_name": "new_view",
            "plone.version": "5.1",
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()  # pre/render/post
