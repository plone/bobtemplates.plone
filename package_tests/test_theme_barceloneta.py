# -*- coding: utf-8 -*-

from .base import init_package_base_structure
from bobtemplates.plone import base
from bobtemplates.plone import theme_barceloneta
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import os
import pytest


def test_pre_theme_name():
    configurator = Configurator(
        template="bobtemplates.plone:theme_barceloneta",
        target_directory="collective.theme",
    )
    question = Question("package", "type")
    theme_barceloneta.pre_theme_name(configurator, question)
    theme_barceloneta.pre_theme_name(configurator, question)


def test_post_theme_name(tmpdir):
    target_path = tmpdir.strpath + "/collective.theme"
    configurator = Configurator(
        template="bobtemplates.plone:theme_barceloneta", target_directory=target_path
    )

    theme_barceloneta.post_theme_name(configurator, None, "collective.theme")
    with pytest.raises(ValidationError):
        theme_barceloneta.post_theme_name(configurator, None, "collective.$SPAM")


def test_prepare_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:theme_barceloneta",
        target_directory=package_path,
        variables={
            "theme.name": "test.theme",
        },
    )
    theme_barceloneta.prepare_renderer(configurator)

    assert configurator.variables["template_id"] == "theme_barceloneta"
    assert configurator.variables["theme.normalized_name"] == "test.theme"
    assert configurator.target_directory.endswith("collective.todo")  # NOQA: E501


def test_post_renderer(tmpdir):
    package_root = tmpdir.strpath + "/collective.todo"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:theme_barceloneta",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={"plone.version": "5.1", "theme.name": "My Theme"},
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()  # pre/render/post
