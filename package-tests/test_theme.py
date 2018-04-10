# -*- coding: utf-8 -*-

from bobtemplates.plone import base
from bobtemplates.plone import theme
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import pytest
import os


def test_pre_theme_name():
    configurator = Configurator(
        template='bobtemplates.plone:theme',
        target_directory='collective.foo',
    )
    question = Question(
        'package',
        'type',
    )
    theme.pre_theme_name(configurator, question)
    theme.pre_theme_name(configurator, question)


def test_post_theme_name(tmpdir):
    target_path = tmpdir.strpath + '/collective.theme'
    configurator = Configurator(
        template='bobtemplates.plone:theme',
        target_directory=target_path,
    )

    theme.post_theme_name(configurator, None, 'collective.theme')
    with pytest.raises(ValidationError):
        theme.post_theme_name(configurator, None, 'collective.$SPAM')


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:theme_package',
        target_directory='collective.foo',
        variables={
            'theme.name': 'test.theme',
        },
    )
    theme.prepare_renderer(configurator)

    assert configurator.variables['template_id'] == 'theme'
    assert configurator.variables['theme.normalized_name'] == 'test.theme'


def test_post_renderer(tmpdir):
    target_path = tmpdir.strpath + '/collective.theme'
    package_path = target_path + '/src/collective/theme'
    profiles_path = package_path + '/profiles/default'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profiles_path)

    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + '/metadata.xml'), 'w') as f:
        f.write(template)

    template = """
[main]
version=5.1
"""
    with open(os.path.join(target_path + '/bobtemplate.cfg'), 'w') as f:
        f.write(template)

    template = """
    dummy
    '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + '/setup.py'), 'w') as f:
        f.write(template)

    template = """
    <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone">

    <!-- -*- extra stuff goes here -*- -->

    </configure>
"""
    with open(os.path.join(package_path + '/configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:theme',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'plone.version': '5.1',
            'theme.name': 'My Theme',
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    theme.prepare_renderer(configurator)
    configurator.render()
    theme.post_renderer(configurator)
