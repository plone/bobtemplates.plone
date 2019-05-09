# -*- coding: utf-8 -*-

from bobtemplates.eea import base
from bobtemplates.eea import restapi_service
from mrbob.configurator import Configurator

import os


def test_pre_renderer(tmpdir):
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    os.makedirs(target_path)
    os.makedirs(package_path)
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

    configurator = Configurator(
        template='bobtemplates.eea:restapi_service',
        target_directory=target_path,
        variables={
            'service_class_name': 'SomeRelatedThings',
            'service_name': 'some-related-things',
            'package_folder': package_path,
        },
    )
    restapi_service.pre_renderer(configurator)


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
        template='bobtemplates.eea:restapi_service',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'package_folder': package_path,
            'plone.version': '5.1',
            'service_class_name': 'SomeRelatedThings',
            'service_name': 'some-related-things',
        },
    )
    assert configurator
    os.chdir(package_path)
    base.set_global_vars(configurator)
    restapi_service.pre_renderer(configurator)
    configurator.render()
    restapi_service.post_renderer(configurator)


def test_remove_unwanted_files(tmpdir):
    files_to_remove = [
        '/api/configure.zcml.example',
        '/api/services/configure.zcml.example',
    ]
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    os.makedirs(package_path + '/api/services/')
    configurator = Configurator(
        template='bobtemplates.eea:restapi_service',
        target_directory=tmpdir.strpath,
        variables={
            'package_folder': package_path,
        },
    )
    for file_to_remove in files_to_remove:
        with open(
            os.path.join(
                package_path + file_to_remove,
            ),
            'w',
        ) as f:
            f.write(u'dummy')
    restapi_service._remove_unwanted_files(configurator)

    for file_to_remove in files_to_remove:
        assert not os.path.isfile(
            os.path.join(package_path + file_to_remove),
        )


def test_update_api_configure_zcml(tmpdir):
    """
    """
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    os.makedirs(package_path + '/api/')

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
    with open(os.path.join(package_path + '/api/configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.eea:restapi_service',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'package_folder': package_path,
            'plone.version': '5.1',
            'service_class_name': 'SomeRelatedThings',
            'service_name': 'some-related-things',
        },
    )
    restapi_service._update_api_configure_zcml(configurator)

    with open(
        os.path.join(
            package_path + '/api/configure.zcml',
        ),
        'r',
    ) as f:
        content = f.read()
        assert content != template, u'configure.zcml was not updated!'


def test_update_services_configure_zcml(tmpdir):
    """
    """
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    os.makedirs(package_path + '/api/services/')

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
    with open(os.path.join(package_path + '/api/configure.zcml'), 'w') as f:
        f.write(template)
    with open(
        os.path.join(package_path + '/api/services/configure.zcml'), 'w',
    ) as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.eea:restapi_service',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'package_folder': package_path,
            'plone.version': '5.1',
            'service_class_name': 'SomeRelatedThings',
            'service_class_name_normalized': 'some_related_things',
            'service_name': 'some-related-things',
        },
    )
    restapi_service._update_services_configure_zcml(configurator)

    with open(
        os.path.join(
            package_path + '/api/services/configure.zcml',
        ),
        'r',
    ) as f:
        content = f.read()
        assert content != template, u'configure.zcml was not updated!'
