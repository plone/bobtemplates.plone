# -*- coding: utf-8 -*-

from bobtemplates.plone import buildout
from mrbob.configurator import Configurator

import os.path


def test_prepare_renderer(buildpath):
    configurator = Configurator(
        template='bobtemplates.plone:buildout',
        target_directory=os.path.join(buildpath, 'test.buildout'),
    )
    buildout.prepare_renderer(configurator)
    assert configurator.variables['template_id'] == 'buildout'


def test_post_renderer():
    buildout.post_renderer(None)
