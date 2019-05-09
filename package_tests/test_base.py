# -*- coding: utf-8 -*-

from bobtemplates.eea import base
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import os
import pytest


def test_to_boolean():
    response_positive = ['Yes', '1', 'y', 'Y', 'True', True, 1]
    resoponse_negative = ['No', '0', 'n', 'N', 'False', False, 0, None]
    for i in range(len(response_positive)):
        assert base.to_boolean(response_positive[i]) is True
        assert base.to_boolean(resoponse_negative[i]) is False


def test_check_klass_name():
    """Test validation of entered class names
    """
    def hookit(value):
        return base.check_klass_name(None, None, value)

    with pytest.raises(ValidationError):
        hookit('import')
    with pytest.raises(ValidationError):
        hookit(u'süpertype')
    with pytest.raises(ValidationError):
        hookit(u'2ndComing')
    with pytest.raises(ValidationError):
        hookit(u'*sterisk')
    assert hookit(u'Supertype') == u'Supertype'
    assert hookit(u'second_coming') == u'second_coming'


def test_read_bobtemplate_ini(tmpdir):
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory='collective.todo',
    )
    base.read_bobtemplates_ini(configurator)

    template = """[main]
version=5.1
"""
    target_dir = tmpdir.strpath + '/collective.foo'
    os.mkdir(target_dir)
    with open(os.path.join(target_dir + '/bobtemplate.cfg'), 'w') as f:
        f.write(template)

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
    )
    base.read_bobtemplates_ini(configurator)


def test_set_global_vars(tmpdir):
    template = """
[main]
version=5.1
"""
    target_dir = tmpdir.strpath + '/collective.foo'
    os.mkdir(target_dir)
    with open(os.path.join(target_dir + '/bobtemplate.cfg'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
        variables={
            'year': 1970,
            'plone.version': '5.1-latest',
        },
    )
    base.set_global_vars(configurator)

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
        variables={
            'year': 1970,
        },
    )
    base.set_global_vars(configurator)


def test_set_plone_version_variables(tmpdir):
    template = """
[main]
version=5.1
"""
    target_dir = tmpdir.strpath + '/collective.foo'
    os.mkdir(target_dir)
    with open(os.path.join(target_dir + '/bobtemplate.cfg'), 'w') as f:
        f.write(template)

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
        variables={
            'plone.version': '5',
        },
    )
    base.set_plone_version_variables(configurator)
    assert configurator.variables.get('plone.is_plone5')
    assert not configurator.variables.get('plone.is_plone51')
    assert not configurator.variables.get('plone.is_plone52')
    assert configurator.variables.get('plone.minor_version') == '5'

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
        variables={
            'plone.version': '5.2',
        },
    )
    base.set_plone_version_variables(configurator)
    assert configurator.variables.get('plone.is_plone5')
    assert not configurator.variables.get('plone.is_plone51')
    assert configurator.variables.get('plone.is_plone52')
    assert configurator.variables.get('plone.minor_version') == '5.2'

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
        variables={
            'plone.version': '5.1',
        },
    )
    base.set_plone_version_variables(configurator)
    assert configurator.variables.get('plone.is_plone5')
    assert configurator.variables.get('plone.is_plone51')
    assert not configurator.variables.get('plone.is_plone52')
    assert configurator.variables.get('plone.minor_version') == '5.1'

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=target_dir,
        variables={
            'plone.version': '4.3',
        },
    )
    base.set_plone_version_variables(configurator)
    assert not configurator.variables.get('plone.is_plone5')
    assert not configurator.variables.get('plone.is_plone51')
    assert not configurator.variables.get('plone.is_plone52')
    assert configurator.variables.get('plone.minor_version') == '4.3'


def test_dottedname_to_path():
    dottedname = 'collective.todo.content'
    assert base.dottedname_to_path(dottedname) == 'collective/todo/content'


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


def test_update_file(tmpdir):
    match_str = '-*- extra stuff goes here -*-'
    path = tmpdir.strpath + '/configure.zcml'
    template = """Some text

    {0}
""".format(
        match_str,
    )
    with open(os.path.join(path), 'w') as f:
        f.write(template)

    base.update_file(None, path, match_str, 'INSERTED')
    assert base.is_string_in_file(None, path, 'INSERTED') is True


def test_subtemplate_warning_post_question():
    assert base.subtemplate_warning_post_question(
        None,
        None,
        'y',
    ) == 'y'
    with pytest.raises(SystemExit):
        base.subtemplate_warning_post_question(None, None, 'n')


def test_validate_packagename(tmpdir):
    base_path = tmpdir.strpath
    # step 1: test None
    with pytest.raises(AttributeError):
        base.validate_packagename(None)

    # step 2: test base namespace (level 2)
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=os.path.join(
            base_path,
            'collective.foo',
        ),
    )
    base.validate_packagename(configurator)

    # step 3: test nested namespace (level 3)
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory=os.path.join(
            base_path,
            'collective.foo.bar',
        ),
    )
    base.validate_packagename(configurator)

    # step 4: test without namespace (level 1)
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.eea:addon',
            target_directory=os.path.join(
                base_path,
                'foo',
            ),
        )
        base.validate_packagename(configurator)

    # step 5: test deep nested namespace (level 4)
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.eea:addon',
            target_directory=os.path.join(
                base_path,
                'collective.foo.bar.spam',
            ),
        )
        base.validate_packagename(configurator)

    # step 6: test leading dot
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.eea:addon',
            target_directory=os.path.join(
                base_path,
                '.collective.foo',
            ),
        )
        base.validate_packagename(configurator)

    # step 7: test ending dot
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.eea:addon',
            target_directory=os.path.join(
                base_path,
                'collective.foo.',
            ),
        )
        base.validate_packagename(configurator)

    # step 8: test invalid char
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.eea:addon',
            target_directory=os.path.join(
                base_path,
                'collective.$SPAM',
            ),
        )
        base.validate_packagename(configurator)


def test_pre_username():
    # step 1: test None
    with pytest.raises(AttributeError):
        base.pre_username(None, None)

    # step 2: test base namespace
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        bobconfig={
            'non_interactive': True,
        },
        target_directory='collective.foo',
    )
    base.pre_username(configurator, None)

    # step 3: test invalid name
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        bobconfig={
            'non_interactive': True,
        },
        target_directory='collective foo',
    )
    with pytest.raises(SystemExit):
        base.pre_username(configurator, None)


def test_pre_email():
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        bobconfig={
            'non_interactive': True,
        },
        target_directory='collective.foo',
    )
    base.pre_email(configurator, None)


def test_post_plone_version():
    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory='collective.foo',
    )
    base.post_plone_version(configurator, None, '4.3')

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory='collective.foo',
    )
    base.post_plone_version(configurator, None, '4-latest')

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory='collective.foo',
    )
    base.post_plone_version(configurator, None, '5.1')

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory='collective.foo',
    )
    base.post_plone_version(configurator, None, '5-latest')

    configurator = Configurator(
        template='bobtemplates.eea:addon',
        target_directory='collective.foo',
        variables={
            'plone.is_plone5': True,
            'plone.minor_version': '5.0',
        },
    )
    base.post_plone_version(configurator, None, '5.0.1')
