# -*- coding: utf-8 -*-

from bobtemplates.eea import base
from bobtemplates.eea import behavior
from mrbob.configurator import Configurator

import os


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.eea:behavior',
        target_directory='.',
        variables={
            'behavior_name': 'AttachmentType',
        },
    )
    assert configurator
    behavior.prepare_renderer(configurator)


def test_post_renderer(tmpdir):
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
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
        template='bobtemplates.eea:behavior',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'plone.version': '5.1',
            'behavior_name': 'AttachmentType',
            'behavior_description': 'Bla',
        },
    )

    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    behavior.prepare_renderer(configurator)
    configurator.render()
    behavior.post_renderer(configurator)
