# -*- coding: utf-8 -*-

from bobtemplates.plone import theme
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import pytest


def test_pre_theme_name():
    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory='collective.foo',
    )
    question = Question(
        'package',
        'type',
    )
    theme.pre_theme_name(configurator, question)
    theme.pre_theme_name(configurator, question)


def test_post_theme_name():
    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory='collective.foo',
    )

    theme.post_theme_name(configurator, None, 'collective.theme')
    with pytest.raises(ValidationError):
        theme.post_theme_name(configurator, None, 'collective.$SPAM')
