# -*- coding: utf-8 -*-

from bobtemplates.plone import theme_package
from mrbob.configurator import Configurator


def test_pre_render():
    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory='collective.theme',
        variables={
            'theme.name': 'Test Theme',
        },
    )
    theme_package.pre_render(configurator)


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
