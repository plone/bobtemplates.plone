# -*- coding: utf-8 -*-

from bobtemplates.plone import base
from mrbob.configurator import Configurator


def test_read_setup_cfg():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    base.read_setup_cfg(configurator)


def test_set_global_vars():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
        variables={
            'year': 1970,
            'plone-version': '5.0-latest',
        }
    )
    base.set_global_vars(configurator)

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
        variables={
            'year': 1970,
        }
    )
    base.set_global_vars(configurator)
