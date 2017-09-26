# -*- coding: utf-8 -*-

from bobtemplates.plone import hooks
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import pytest


def test_to_boolean():
    # Initial simple test to show coverage in hooks.py.

    # Positive Return Checks
    assert hooks.to_boolean(None, None, True)
    assert hooks.to_boolean(None, None, 'y')
    assert hooks.to_boolean(None, None, 'yes')
    assert hooks.to_boolean(None, None, 'true')
    assert hooks.to_boolean(None, None, '1')

    # Negative Return Checks
    assert hooks.to_boolean(None, None, False) is False
    assert hooks.to_boolean(None, None, 'n') is False
    assert hooks.to_boolean(None, None, 'no') is False
    assert hooks.to_boolean(None, None, 'false') is False
    assert hooks.to_boolean(None, None, '0') is False

    # Error Check
    with pytest.raises(ValidationError, msg='Value must be a boolean (y/n)'):
        assert hooks.to_boolean(None, None, 'spam')


def test_validate_packagename():
    # step 1: test None
    with pytest.raises(AttributeError):
        hooks.validate_packagename(None)

    # step 2: test base namespace (level 2)
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.validate_packagename(configurator)

    # step 3: test without namespace (level 1)
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.plone:addon',
            target_directory='foo',
        )
        hooks.validate_packagename(configurator)

    # step 4: test deep nested namespace (level 4)
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.plone:addon',
            target_directory='collective.foo.bar.spam',
        )
        hooks.validate_packagename(configurator)

    # step 5: test leading dot
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.plone:addon',
            target_directory='.collective.foo',
        )
        hooks.validate_packagename(configurator)

    # step 6: test ending dot
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.plone:addon',
            target_directory='collective.foo.',
        )
        hooks.validate_packagename(configurator)

    # step 7: test invalid char
    with pytest.raises(SystemExit):
        configurator = Configurator(
            template='bobtemplates.plone:addon',
            target_directory='collective.$PAM',
        )
        hooks.validate_packagename(configurator)


def test_pre_username():
    # step 1: test None
    with pytest.raises(AttributeError):
        hooks.pre_username(None, None)

    # step 2: test base namespace
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.pre_username(configurator, None)


def test_pre_email():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.pre_email(configurator, None)


def test_post_plone_version():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.post_plone_version(configurator, None, '4.3')

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.post_plone_version(configurator, None, '4-latest')

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.post_plone_version(configurator, None, '5.1')

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
    )
    hooks.post_plone_version(configurator, None, '5-latest')

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo',
        variables={
            'plone.is_plone5': True,
            'plone.minor_version': '5.0',
        },
    )
    hooks.post_plone_version(configurator, None, '5.0.1')


def test_prepare_render():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo.bar',
        variables={
            'package.dexterity_type_name': 'Task',
        },
    )
    hooks.prepare_render(configurator)

    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory='collective.theme',
        variables={
            'theme.name': 'Test Theme',
        },
    )
    hooks.prepare_render(configurator)


def test_cleanup_package():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo.bar',
        variables={
            'package.nested': True,
            'package.namespace': 'collective',
            'package.namespace2': 'foo',
            'package.name': 'bar',
            'year': 1970,
            'description': 'Test',
            'author.name': 'The Plone Collective',
            'author.email': 'collective@plone.org',
            'author.github.user': 'collective',
            'author.irc': 'irc.freenode.org#plone',
            'plone.version': '5.0.1',
        },
    )
    # configurator.render()
    # hooks.cleanup_package(configurator)
    assert configurator

    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory='collective.theme',
        variables={
            'package.nested': False,
            'package.namespace': 'collective',
            'package.namespace2': '',
            'package.name': 'theme',
            'package.type': 'theme',
            'year': 1970,
            'description': 'Test',
            'author.name': 'The Plone Collective',
            'author.email': 'collective@plone.org',
            'author.github.user': 'collective',
            'author.irc': 'irc.freenode.org#plone',
            'plone.version': '5.0.1',
        },
    )
    # configurator.render()
    # hooks.cleanup_package(configurator)
    assert configurator
