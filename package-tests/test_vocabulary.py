# -*- coding: utf-8 -*-

from bobtemplates.plone import vocabulary
from mrbob.configurator import Configurator


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:vocabulary',
        target_directory='.',
        variables={
            'vocabulary_name': 'ExampleVocabulary',
        },
    )
    vocabulary.prepare_renderer(configurator)
