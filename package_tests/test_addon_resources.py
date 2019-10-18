# -*- coding: utf-8 -*-

from bobtemplates.plone import addon_resources
from bobtemplates.plone import base
from mrbob.configurator import Configurator

import os


def test_pre_render(tmpdir):
    configurator = Configurator(
        template='bobtemplates.plone:addon_resources',
        target_directory=tmpdir.strpath + 'collective.foo',
    )
    addon_resources.pre_render(configurator)

