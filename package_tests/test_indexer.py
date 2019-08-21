# -*- coding: utf-8 -*-

"""Test view generation."""

# from bobtemplates.plone import base
from bobtemplates.plone import indexer
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import os
import pytest


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
  <adapter
    name="{indexer_index_name}"
    factory=".{indexer_file_name}.dummy"
    />
  <adapter
    name="{indexer_index_name}"
    factory=".{indexer_file_name}.handler"
    />

</configure>
"""
    with open(os.path.join(indexers_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:indexer",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "indexer_index_name": "my_cool_index",
            "indexer_indexer_name": "my_cool_indexer",
            "package_folder": package_path,
        },
    )
    indexer._update_indexers_configure_zcml(configurator)

    with open(os.path.join(indexers_path + "configure.zcml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)
