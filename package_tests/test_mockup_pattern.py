# -*- coding: utf-8 -*-
from .base import init_package_base_structure
from bobtemplates.plone import base
from bobtemplates.plone import mockup_pattern
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import os
import pytest


def test_pre_render(tmpdir):
    package_root = tmpdir.strpath + "/collective.testpattern"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:mockup_pattern",
        target_directory=package_path,
        variables={
            "pattern.name": "test-pattern",
        },
    )
    mockup_pattern.pre_render(configurator)

    assert configurator.variables["template_id"] == "mockup_pattern"
    assert configurator.variables["pattern.name"] == "test-pattern"
    assert configurator.target_directory.endswith("collective.testpattern")


def test_post_render(tmpdir):
    package_root = tmpdir.strpath + "/collective.testpattern"
    package_path = init_package_base_structure(package_root)

    configurator = Configurator(
        template="bobtemplates.plone:mockup_pattern",
        target_directory=package_path,
        bobconfig={"non_interactive": True},
        variables={
            "plone.version": "6.0",
            "pattern.name": "test-pattern",
        },
    )
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


def test_post_pattern_name(tmpdir):
    """Verifies that pattern names are checked for validity."""
    target_path = tmpdir.strpath + "/collective.testpattern"
    configurator = Configurator(
        template="bobtemplates.plone:mockup_pattern", target_directory=target_path
    )

    mockup_pattern.post_pattern_name(configurator, None, "test-pattern")
    with pytest.raises(ValidationError):
        mockup_pattern.post_pattern_name(configurator, None, "test.$SPAM")
