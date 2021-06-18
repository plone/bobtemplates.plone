# -*- coding: utf-8 -*-

"""Test view generation."""

import os

import pytest
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

from bobtemplates.plone import base, indexer

from .base import init_package_base_structure


def test_update_indexers_configure_zcml(tmpdir):
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    indexers_path = package_path + "/indexers/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(indexers_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

</configure>
"""
    with open(os.path.join(indexers_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:indexer",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "indexer_name": "my_cool_index",
            "package_folder": package_path,
        },
    )
    indexer._update_indexers_configure_zcml(configurator)

    with open(os.path.join(indexers_path + "configure.zcml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_pre_renderer(tmpdir):
    base_path = tmpdir.strpath
    package_root_folder = os.path.join(
        base_path,
        "collective.foo",
    )
    package_path = init_package_base_structure(package_root_folder)
    configurator = Configurator(
        template="bobtemplates.plone:indexer",
        bobconfig={"non_interactive": True},
        target_directory=package_path,
        variables={
            "package.root_folder": package_root_folder,
            "indexer_name": "my_cool_index",
            "package_folder": os.path.join(
                package_root_folder,
                "src/collective/foo",
            ),
        },
    )
    indexer.pre_renderer(configurator)


def test_post_renderer(tmpdir):
    base_path = tmpdir.strpath
    package_root_folder = os.path.join(
        base_path,
        "collective.foo",
    )
    package_path = init_package_base_structure(package_root_folder)
    configurator = Configurator(
        template="bobtemplates.plone:indexer",
        bobconfig={"non_interactive": True},
        target_directory=package_path,
        variables={
            "package.root_folder": package_root_folder,
            "indexer_name": "my_cool_index",
            "package_folder": package_path,
        },
    )
    # os.makedirs(target_path)

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

    os.chdir(package_path)
    base.set_global_vars(configurator)
    configurator.render()
