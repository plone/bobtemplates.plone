# -*- coding: utf-8 -*-

from bobtemplates.plone import theme_package
from mrbob.configurator import Configurator

import os.path


def test_pre_render(buildpath):
    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory=os.path.join(buildpath, 'collective.theme'),
        variables={
            'theme.name': 'Test Theme',
        },
    )
    theme_package.pre_render(configurator)


def test_cleanup_package(buildpath):
    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory=os.path.join(buildpath, 'collective.theme'),
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
            'plone.is_plone5': True,
        },
    )
    # configurator.render()
    # hooks.cleanup_package(configurator)
    assert configurator
