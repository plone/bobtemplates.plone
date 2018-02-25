# -*- coding: utf-8 -*-

from bobtemplates.plone import behavior
from mrbob.configurator import Configurator


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:behavior',
        target_directory='.',
        variables={
            'behavior_name': 'AttachmentType',
        },
    )
    behavior.prepare_renderer(configurator)
