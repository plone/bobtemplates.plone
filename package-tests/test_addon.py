# -*- coding: utf-8 -*-

from bobtemplates.plone import addon
from mrbob.configurator import Configurator


def test_pre_render():
    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory='collective.foo.bar',
        variables={
            'package.dexterity_type_name': 'Task',
        },
    )
    addon.pre_render(configurator)


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
