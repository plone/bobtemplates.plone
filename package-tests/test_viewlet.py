# -*- coding: utf-8 -*-

"""Test view generation."""

from bobtemplates.plone import base
from bobtemplates.plone import viewlet
from mrbob.bobexceptions import SkipQuestion
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import os
import pytest


def test_get_view_name_default():
    question = Question(name='view_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_python_class_name': 'DemoViewlet',
        },
    )
    viewlet.get_view_name_from_python_class(configurator, question)


def test_get_template_name_default():
    question = Question(name='viewlet_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_template': False,
        },
    )
    viewlet.get_template_name_default(configurator, question)


def test_get_template_name():
    question = Question(name='viewlet_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_template': True,
            'viewlet_name': 'myviewlet',
        },
    )
    viewlet.get_template_name_default(configurator, question)


def test_viewlet_template_true():
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_template': True,
        },
    )
    viewlet.check_viewlet_template_answer(configurator, None)


def test_viewlet_template_false():
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_template': False,
        },
    )
    with pytest.raises(SkipQuestion):
        viewlet.check_viewlet_template_answer(configurator, None)


def test_update_configure_zcml(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + '/collective.demo'
    package_path = target_path + '/src/collective/demo'
    os.makedirs(target_path)
    os.makedirs(package_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.demo">

  <i18n:registerTranslations directory="locales" />

  <!--<includeDependencies package="." />-->

  <include package=".viewlets" />

  <include package=".browser" />

</configure>
"""
    with open(os.path.join(package_path + '/configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.demo',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'package_folder': package_path,
        },
    )
    viewlet._update_configure_zcml(configurator)

    with open(os.path.join(package_path + '/configure.zcml'), 'r') as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_viewlets_configure_zcml_with_template(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    viewlets_path = package_path + '/viewlets/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(viewlets_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.sample">

  -*- extra stuff goes here -*-
  <browser:viewlet
     name="viewlet"
     for="*"
     manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
     layer="collective.sample.interfaces.ICollectiveTodoLayer"
     class=".py_viewlet.MyViewlet"
     template="pt_viewlet.pt"
     permission="zope2.View"
     />


</configure>
"""
    with open(os.path.join(viewlets_path + 'configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_name': 'viewlet',
            'viewlet_python_class_name': 'MyViewlet',
            'viewlet_python_file_name': 'py_viewlet',
            'viewlet_template': True,
            'viewlet_template_name': 'pt_viewlet',
            'package_folder': package_path,
            'package.dottedname': 'collective.sample',
            'browser_layer': 'ICollectiveSampleLayer',
        },
    )
    viewlet._update_viewlets_configure_zcml(configurator)

    with open(os.path.join(viewlets_path + 'configure.zcml'), 'r') as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_viewlets_configure_zcml_without_template(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    viewlets_path = package_path + '/viewlets/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(viewlets_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.sample">

  -*- extra stuff goes here -*-
  <browser:viewlet
     name="viewlet"
     for="*"
     manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
     layer="collective.sample.interfaces.ICollectiveTodoLayer"
     class=".py_viewlet.MyViewlet"
     permission="zope2.View"
     />


</configure>
"""
    with open(os.path.join(viewlets_path + 'configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_name': 'viewlet',
            'viewlet_python_class_name': 'MyViewlet',
            'viewlet_python_file_name': 'py_viewlet',
            'viewlet_template': False,
            'package_folder': package_path,
            'package.dottedname': 'collective.sample',
            'browser_layer': 'ICollectiveSampleLayer',
        },
    )
    viewlet._update_viewlets_configure_zcml(configurator)

    with open(os.path.join(viewlets_path + 'configure.zcml'), 'r') as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_delete_template_file(tmpdir):
    """Test to remove unwanted file."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    viewlets_path = package_path + '/viewlets/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(viewlets_path)
    file_name = u'configure.zcml.example'
    file_path = viewlets_path + file_name
    open(file_path, 'a').close()
    file_name = u'my_viewlet.pt'
    file_path = viewlets_path + file_name
    open(file_path, 'a').close()
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_name_normalized': 'my_viewlet',
            'viewlet_template': False,
            'viewlet_template_name': 'my_viewlet',
            'package_folder': package_path,
        },
    )
    viewlet._delete_unwanted_files(configurator)
    if os.path.isfile(file_path):
        pytest.raises(ValidationError)


def test_delete_template_file_false(tmpdir):
    """Test to not remove template file."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    viewlets_path = package_path + '/viewlets/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(viewlets_path)
    file_name = u'configure.zcml.example'
    file_path = viewlets_path + file_name
    open(file_path, 'a').close()
    file_name = u'my_viewlet.pt'
    file_path = viewlets_path + file_name
    open(file_path, 'a').close()
    configurator = Configurator(
        template='bobtemplates.plone:viewlet',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_name_normalized': 'my_viewlet',
            'viewlet_template': True,
            'viewlet_template_name': 'my_viewlet',
            'package_folder': package_path,
        },
    )
    viewlet._delete_unwanted_files(configurator)
    if not os.path.isfile(file_path):
        pytest.raises(ValidationError)


def test_post_renderer_with_template(tmpdir):
    """Test post rendering."""
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    viewlets_path = package_path + '/viewlets'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(viewlets_path)

    template = """# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class MyViewlet(ViewletBase):

    def render(self):
        return u'Sample viewlet!'

"""
    with open(os.path.join(viewlets_path + '/viewlet.py'), 'w') as f:
        f.write(template)
    template = """<div class="days_to_conf">
    ${view/get_message}
</div>
"""
    with open(os.path.join(viewlets_path + '/viewlet.pt'), 'w') as f:
        f.write(template)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

    -*- extra stuff goes here -*-
    <browser:viewlet
       name="viewlet"
       for="*"
       manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
       layer="collective.todo.interfaces.ICollectiveTodoLayer"
       class=".viewlet.MyViewlet"
       template="viewlet.pt"
       permission="zope2.View"
       />


    </configure>
    """
    with open(os.path.join(viewlets_path + '/configure.zcml'), 'w') as f:
        f.write(template)

    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

  <i18n:registerTranslations directory="locales" />

  <!--
    Be careful if you use general includeDependencies, it can have sideffects!
    Better import explicite packages or configurations ;)
  -->
  <!--<includeDependencies package="." />-->

  <include package=".viewlets" />

</configure>
"""
    with open(os.path.join(package_path + '/configure.zcml'), 'w') as f:
        f.write(template)

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_name': 'viewlet',
            'viewlet_python_class_name': 'MyViewlet',
            'viewlet_template': True,
            'viewlet_template_name': 'viewlet',
            'plone.version': '5.1',
        },
    )

    template = """
        dummy
        '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + '/setup.py'), 'w') as f:
        f.write(template)

    os.chdir(package_path)
    base.set_global_vars(configurator)
    viewlet.prepare_renderer(configurator)
    viewlet.post_renderer(configurator)


def test_post_renderer_without_template(tmpdir):
    """Test post rendering."""
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    viewlets_path = package_path + '/viewlets'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(viewlets_path)

    template = """# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class MyViewlet(ViewletBase):

    def render(self):
        return u'Sample viewlet!'

"""
    with open(os.path.join(viewlets_path + '/viewlet.py'), 'w') as f:
        f.write(template)
    template = """<div class="days_to_conf">
    ${view/get_message}
</div>
"""
    with open(os.path.join(viewlets_path + '/viewlet.pt'), 'w') as f:
        f.write(template)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

    -*- extra stuff goes here -*-
    <browser:viewlet
       name="viewlet"
       for="*"
       manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
       layer="collective.todo.interfaces.ICollectiveTodoLayer"
       class=".viewlet.MyViewlet"
       template="viewlet.pt"
       permission="zope2.View"
       />


    </configure>
    """
    with open(os.path.join(viewlets_path + '/configure.zcml'), 'w') as f:
        f.write(template)

    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

  <i18n:registerTranslations directory="locales" />

  <!--
    Be careful if you use general includeDependencies, it can have sideffects!
    Better import explicite packages or configurations ;)
  -->
  <!--<includeDependencies package="." />-->

  <include package=".viewlets" />

</configure>
"""
    with open(os.path.join(package_path + '/configure.zcml'), 'w') as f:
        f.write(template)

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory=package_path,
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'viewlet_name': 'viewlet',
            'viewlet_python_class_name': 'MyViewlet',
            'viewlet_template': False,
            'plone.version': '5.1',
        },
    )

    template = """
        dummy
        '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + '/setup.py'), 'w') as f:
        f.write(template)

    os.chdir(package_path)
    base.set_global_vars(configurator)
    viewlet.prepare_renderer(configurator)
    viewlet.post_renderer(configurator)
