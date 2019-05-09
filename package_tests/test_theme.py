# -*- coding: utf-8 -*-

from .base import init_package_base_files
from bobtemplates.eea import base
from bobtemplates.eea import theme
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import os
import pytest


def test_pre_theme_name(tmpdir):
    base_path = tmpdir.strpath
    configurator = Configurator(
        template='bobtemplates.eea:theme',
        target_directory=os.path.join(
            base_path,
            'collective.foo',
        ),
    )
    question = Question(
        'package',
        'type',
    )
    theme.pre_theme_name(configurator, question)
    theme.pre_theme_name(configurator, question)


def test_post_theme_name(tmpdir):
    base_path = tmpdir.strpath
    configurator = Configurator(
        template='bobtemplates.eea:theme',
        target_directory=os.path.join(
            base_path,
            'collective.foo',
        ),
    )

    theme.post_theme_name(configurator, None, 'collective.foo')
    with pytest.raises(ValidationError):
        theme.post_theme_name(configurator, None, 'collective.$SPAM')


def test_prepare_renderer(tmpdir):
    base_path = tmpdir.strpath
    package_root_folder = os.path.join(
        base_path,
        'collective.foo',
    )
    configurator = Configurator(
        template='bobtemplates.eea:theme',
        target_directory=os.path.join(
            package_root_folder,
            'src/collective/foo',
        ),
        variables={
            'theme.name': 'test.theme',
            'package.root_folder': package_root_folder,
        },
    )
    init_package_base_files(configurator)
    theme.prepare_renderer(configurator)

    assert configurator.variables['template_id'] == 'theme'
    assert configurator.variables['theme.normalized_name'] == 'test.theme'
    assert configurator.target_directory.endswith('/collective.foo/src/collective/foo')  # NOQA: E501

    # nested namespace package
    package_root_folder = os.path.join(
        base_path,
        'collective.foo.bar',
    )
    configurator = Configurator(
        template='bobtemplates.eea:theme',
        target_directory=os.path.join(
            package_root_folder,
            'src/collective/foo/bar',
        ),
        variables={
            'theme.name': 'test.theme',
            'package.root_folder': package_root_folder,
        },
    )
    init_package_base_files(configurator)
    theme.prepare_renderer(configurator)

    assert configurator.variables['template_id'] == 'theme'
    assert configurator.variables['theme.normalized_name'] == 'test.theme'
    assert configurator.target_directory.endswith('/collective.foo.bar/src/collective/foo/bar')  # NOQA: E501


def test_post_renderer(tmpdir):
    base_path = tmpdir.strpath
    target_path = os.path.join(
        base_path,
        'collective.theme',
    )
    package_path = os.path.join(
        target_path,
        u'src/collective/theme',
    )
    profiles_path = os.path.join(
        package_path,
        u'profiles/default',
    )
    theme_path = os.path.join(
        package_path,
        u'theme',
    )
    os.makedirs(package_path)
    os.makedirs(profiles_path)
    os.makedirs(theme_path)

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
        template='bobtemplates.eea:theme',
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
