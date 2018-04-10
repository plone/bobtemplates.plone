# -*- coding: utf-8 -*-

from bobtemplates.plone import base
from bobtemplates.plone import behavior
from mrbob.configurator import Configurator

import os


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:behavior',
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

    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + '/metadata.xml'), 'w') as f:
        f.write(template)

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'dexterity_type_name': 'Task',
            'plone.version': '5.1',
        },
    )

    os.chdir(package_path)
    base.set_global_vars(configurator)
    behavior.prepare_renderer(configurator)
    behavior.post_renderer(configurator)


#def test__update_package_configure_zcml(tmpdir):
#    """
#    """
#    target_path = tmpdir.strpath + '/collective.todo'
#    package_path = target_path + '/src/collective/todo'
#    os.makedirs(target_path)
#    os.makedirs(package_path)
#
#    configurator = Configurator(
#        template='bobtemplates.plone:behavior',
#        target_directory=package_path,
#        bobconfig={
#            'non_interactive': True,
#        },
#        variables={
#            'behavior_name': 'Task',
#        },
#    )
#    behavior._update_package_configure_zcml(configurator)
#
#
