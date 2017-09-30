# -*- coding: utf-8 -*-

from bobtemplates.plone import vocabulary
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import pytest


def test_post_vocabulary_name():
    def hookit(value):
        return vocabulary.check_vocabulary_name(None, None, value)

    with pytest.raises(ValidationError):
        hookit('import')
    with pytest.raises(ValidationError):
        hookit(u'süpertype')
#    with pytest.raises(ValidationError):
#        hookit(u'Staff Member')
    with pytest.raises(ValidationError):
        hookit(u'2ndComing')
#    with pytest.raises(ValidationError):
#        hookit(u'Second Coming')
    with pytest.raises(ValidationError):
        hookit(u'*sterisk')
    assert hookit(u'Supertype') == u'Supertype'
    assert hookit(u'second_coming') == u'second_coming'
#    assert hookit(u'the_2nd_coming') == u'the_2nd_coming'


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:vocabulary',
        target_directory='.',
        variables={
            'vocabulary_name': 'ExampleVocabulary',
        },
    )
    vocabulary.prepare_renderer(configurator)
