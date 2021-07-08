# -*- coding: utf-8 -*-

import os

import pytest
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator, Question

from bobtemplates.plone import base, theme

from .base import init_package_base_structure


def test_pre_theme_name(tmpdir):
    base_path = tmpdir.strpath
    configurator = Configurator(
        template="bobtemplates.plone:theme",
        target_directory=os.path.join(
            base_path,
            "collective.foo",
        ),
    )
    question = Question(
        "package",
        "type",
    )
    theme.pre_theme_name(configurator, question)
    theme.pre_theme_name(configurator, question)


def test_post_theme_name(tmpdir):
    base_path = tmpdir.strpath
    configurator = Configurator(
        template="bobtemplates.plone:theme",
        target_directory=os.path.join(
            base_path,
            "collective.foo",
        ),
    )

    theme.post_theme_name(configurator, None, "collective.foo")
    with pytest.raises(ValidationError):
        theme.post_theme_name(configurator, None, "collective.$SPAM")


def test_prepare_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:theme",
        target_directory=package_path,
        variables={
            "theme.name": "test.theme",
        },
    )
    theme.prepare_renderer(configurator)

    assert configurator.variables["template_id"] == "theme"
    assert configurator.variables["theme.normalized_name"] == "test.theme"
    assert configurator.target_directory.endswith(
        "/collective.todo/src/collective/todo"
    )  # NOQA: E501

    # nested namespace package
    package_root = os.path.join(
        tmpdir.strpath,
        "collective.foo.bar",
    )
    package_path = init_package_base_structure(package_root)
    configurator = Configurator(
        template="bobtemplates.plone:theme",
        target_directory=package_path,
        variables={
            "theme.name": "test.theme",
            "package.root_folder": package_root,
        },
    )
    theme.prepare_renderer(configurator)

    assert configurator.variables["template_id"] == "theme"
    assert configurator.variables["theme.normalized_name"] == "test.theme"
    assert configurator.target_directory.endswith(
        "/collective.foo.bar/src/collective/foo/bar"
    )  # NOQA: E501


def test_post_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:theme",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={"plone.version": "5.1", "theme.name": "My Theme"},
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    theme.prepare_renderer(configurator)
    configurator.render()
    theme.post_renderer(configurator)
