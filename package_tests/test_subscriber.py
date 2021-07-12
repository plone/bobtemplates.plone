# -*- coding: utf-8 -*-

"""Test view generation."""

import os

import pytest
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

# from bobtemplates.plone import base
from bobtemplates.plone import subscriber


def test_update_subscribers_configure_zcml(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    subscribers_path = package_path + "/subscribers/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(subscribers_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-

  <subscriber for="plone.dexterity.interfaces.IDexterityContent
                   zope.lifecycleevent.interfaces.IObjectModifiedEvent"
              handler=".obj_mod_do_something.handler"
              />

</configure>
"""
    with open(os.path.join(subscribers_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:subscriber",
        target_directory="collective.sample",
        bobconfig={"non_interactive": True},
        variables={
            "subscriber_handler_name": "obj_mod_do_something",
            "subscriber_handler_file_name": "obj_mod_do_something",
            "package_folder": package_path,
        },
    )
    subscriber._update_subscribers_configure_zcml(configurator)

    with open(os.path.join(subscribers_path + "configure.zcml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)
