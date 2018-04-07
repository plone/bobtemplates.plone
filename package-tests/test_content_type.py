# -*- coding: utf-8 -*-

from bobtemplates.plone import base
from bobtemplates.plone import content_type
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import os
import pytest


def test_post_dexterity_type_name():
    """Test validation of entered dexterity type names
    """
    def hookit(value):
        return content_type.check_dexterity_type_name(None, None, value)

    with pytest.raises(ValidationError):
        hookit('import')
    with pytest.raises(ValidationError):
        hookit(u'süpertype')
#    with pytest.raises(ValidationError):
#        hookit(u'Staff Member')
    with pytest.raises(ValidationError):
        hookit(u'2ndComing')
#    with pytest.raises(ValidationError):
#        hookit(u'Second Coming')
    with pytest.raises(ValidationError):
        hookit(u'*sterisk')
    assert hookit(u'Supertype') == u'Supertype'
    assert hookit(u'second_coming') == u'second_coming'
#    assert hookit(u'the_2nd_coming') == u'the_2nd_coming'


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:content_type',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'dexterity_type_name': 'Task',
        },
    )
    content_type.prepare_renderer(configurator)


def test_post_renderer(tmpdir):
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    profiles_path = package_path + '/profiles/default'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profiles_path + '/types')

    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + '/metadata.xml'), 'w') as f:
        f.write(template)

    template = """<?xml version="1.0"?>
<rolemap>
  <permissions>
  <!-- -*- extra stuff goes here -*- -->

  </permissions>
</rolemap>
"""
    with open(os.path.join(profiles_path + '/rolemap.xml'), 'w') as f:
        f.write(template)

    template = """<?xml version="1.0"?>
<object name="portal_types" meta_type="Plone Types Tool">
 <property name="title">Controls the available contenttypes in your portal
 </property>
 <!--<object name="example_ct" meta_type="Dexterity FTI"/>-->
</object>
"""
    with open(os.path.join(profiles_path + '/types.xml'), 'w') as f:
        f.write(template)

    template = """<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:zcml="http://namespaces.zope.org/zcml"
  i18n_domain="plone">

  <configure zcml:condition="installed AccessControl.security">
  <!-- -*- extra stuff goes here -*- -->


  </configure>

</configure>
"""
    with open(os.path.join(package_path + '/permissions.zcml'), 'w') as f:
        f.write(template)

    template = """
[tool:bobtemplates.plone]
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
    content_type.prepare_renderer(configurator)
    content_type.post_renderer(configurator)
