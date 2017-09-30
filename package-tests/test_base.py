# -*- coding: utf-8 -*-

from bobtemplates.plone import base
from mrbob.configurator import Configurator

import os
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


def test_is_string_in_file(tmpdir):
    match_str = '-*- extra stuff goes here -*-'
    path = tmpdir.strpath + '/configure.zcml'
    template = """Some text

    {0}
""".format(
        match_str,
    )
    with open(os.path.join(path), 'w') as f:
        f.write(template)

    assert base.is_string_in_file(None, path, match_str) is True
    assert base.is_string_in_file(None, path, 'hello') is False


def test_subtemplate_warning_post_question():
    assert base.subtemplate_warning_post_question(None, None, 'YES') == 'YES'
    with pytest.raises(SystemExit):
        base.subtemplate_warning_post_question(None, None, 'No')
