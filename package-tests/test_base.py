# -*- coding: utf-8 -*-

from bobtemplates.plone import base
from mrbob.configurator import Configurator

import pytest


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
        },
    )
    base.set_global_vars(configurator)

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
        variables={
            'year': 1970,
        },
    )
    base.set_global_vars(configurator)


def test_subtemplate_warning(capsys):
    base.subtemplate_warning(None, None)
    out, err = capsys.readouterr()
    assert '### WARNING ###' in out
    assert err == ''


def test_subtemplate_warning_post_question():
    assert base.subtemplate_warning_post_question(None, None, 'YES') == 'YES'
    with pytest.raises(SystemExit):
        base.subtemplate_warning_post_question(None, None, 'No')
