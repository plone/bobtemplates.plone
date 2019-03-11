# -*- coding: utf-8 -*-

"""Test view generation."""

from bobtemplates.plone import base
from bobtemplates.plone import view
from mrbob.bobexceptions import SkipQuestion
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator
from mrbob.configurator import Question

import os
import pytest


def test_get_view_name_default():
    question = Question(name='view_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': False,
        },
    )
    view.get_view_name_from_python_class(configurator, question)


def test_get_view_name():
    question = Question(name='view_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
            'view_python_class_name': 'DemoView',
        },
    )
    view.get_view_name_from_python_class(configurator, question)


def test_get_template_name_default():
    question = Question(name='view_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_template': False,
        },
    )
    view.get_template_name_default(configurator, question)


def test_get_template_name():
    question = Question(name='view_name', question='', default=None)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_template': True,
            'view_name': 'my-view',
        },
    )
    view.get_template_name_default(configurator, question)


def test_python_class_true():
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
        },
    )
    view.check_python_class_answer(configurator, None)


def test_python_class_false():
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': False,
        },
    )
    with pytest.raises(SkipQuestion):
        view.check_python_class_answer(configurator, None)


def test_view_template_true():
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
            'view_template': True,
        },
    )
    view.check_view_template_answer(configurator, None)


def test_view_template_false():
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
            'view_template': False,
        },
    )
    with pytest.raises(SkipQuestion):
        view.check_view_template_answer(configurator, None)


def test_view_template_and_python_class_false():
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': False,
            'view_template': False,
        },
    )
    with pytest.raises(ValidationError):
        view.check_view_template_answer(configurator, None)


def test_update_views_configure_zcml(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    views_path = package_path + '/views/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-
  <browser:page
     name="py_view"
     for="*"
     class=".py_view.MyView"
     template="pt_view.pt"
     permission="zope2.View"
     />


</configure>
"""
    with open(os.path.join(views_path + 'configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
            'view_python_class_name': 'MyView',
            'view_python_file_name': 'py_view',
            'view_name': 'py-view',
            'view_template': True,
            'view_template_name': 'pt_view',
            'package_folder': package_path,
        },
    )
    view._update_views_configure_zcml(configurator)

    with open(os.path.join(views_path + 'configure.zcml'), 'r') as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_views_configure_zcml_without_template(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    views_path = package_path + '/views/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-
  <browser:page
     name="py_view"
     for="*"
     class=".py_view.MyView"
     permission="zope2.View"
     />


</configure>
"""
    with open(os.path.join(views_path + 'configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
            'view_python_class_name': 'MyView',
            'view_python_file_name': 'py_view',
            'view_name': 'py-view',
            'view_template': False,
            'package_folder': package_path,
        },
    )
    view._update_views_configure_zcml(configurator)

    with open(os.path.join(views_path + 'configure.zcml'), 'r') as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_views_configure_zcml_without_python_class(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    views_path = package_path + '/views/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="{{{ package.dottedname }}}">

  -*- extra stuff goes here -*-
  <browser:page
     name="py_view"
     for="*"
     template="pt_view.pt"
     permission="zope2.View"
     />


</configure>
"""
    with open(os.path.join(views_path + 'configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': False,
            'view_name': 'py-view',
            'view_template': True,
            'view_template_name': 'pt_view',
            'package_folder': package_path,
        },
    )
    view._update_views_configure_zcml(configurator)

    with open(os.path.join(views_path + 'configure.zcml'), 'r') as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_file_names(tmpdir):
    """Test files names of template and Python class file."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    views_path = package_path + '/views/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    python_file_name = u'my_view.py'
    python_file_path = views_path + python_file_name
    open(python_file_path, 'a').close()
    template_file_name = u'my-view.pt'
    template_file_path = views_path + template_file_name
    open(template_file_path, 'a').close()
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_python_class': True,
            'view_name_normalized': 'my_view',
            'view_template': True,
            'view_template_name': 'my-view',
            'view_name_normalized': 'my_view',
            'view_python_file_name': 'my_view',
            'package_folder': package_path,
        },
    )
    view._delete_unwanted_files(configurator)
    if not os.path.isfile(template_file_path):
        pytest.raises(ValidationError)

    if not os.path.isfile(python_file_path):
        pytest.raises(ValidationError)


def test_delete_template_file(tmpdir):
    """Test to remove unwanted files."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    views_path = package_path + '/views/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    file_name = u'configure.zcml.example'
    file_path = views_path + file_name
    open(file_path, 'a').close()
    file_name = u'my-view.pt'
    file_path = views_path + file_name
    open(file_path, 'a').close()
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_name': 'my-view',
            'view_python_class': True,
            'view_template_name': 'my-view',
            'view_template': False,
            'package_folder': package_path,
        },
    )
    view._delete_unwanted_files(configurator)
    if os.path.isfile(file_path):
        pytest.raises(ValidationError)


def test_delete_python_file(tmpdir):
    """Test to remove unwanted files."""
    target_path = tmpdir.strpath + '/collective.sample'
    package_path = target_path + '/src/collective/sample'
    views_path = package_path + '/views/'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)
    file_name = u'configure.zcml.example'
    file_path = views_path + file_name
    open(file_path, 'a').close()
    file_name = u'myview.py'
    file_path = views_path + file_name
    open(file_path, 'a').close()
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.sample',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'view_name': 'myview',
            'view_python_class': False,
            'view_python_file_name': 'myview',
            'view_template': True,
            'package_folder': package_path,
        },
    )
    view._delete_unwanted_files(configurator)
    if os.path.isfile(file_path):
        pytest.raises(ValidationError)


def test_update_configure_zcml(tmpdir):
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

  <include package=".browser" />

</configure>
"""
    with open(os.path.join(package_path + '/configure.zcml'), 'w') as f:
        f.write(template)
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.demo',
        bobconfig={
            'non_interactive': True,
        },
        variables={
            'package_folder': package_path,
        },
    )
    view._update_configure_zcml(configurator)


def test_post_renderer(tmpdir):
    """Test post rendering."""
    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    views_path = package_path + '/views'
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(views_path)

    template = """# -*- coding: utf-8 -*-

from collective.todo import _
from Products.Five.browser import BrowserView


class MyView(BrowserView):

    def __call__(self):
        return _(u'This view works!')

"""
    with open(os.path.join(views_path + '/view.py'), 'w') as f:
        f.write(template)
    template = """<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="collective.todo"
      metal:use-macro="context/main_template/macros/master">
<body>
    <metal:block fill-slot="content-core">
        <li class="heading" i18n:translate="">
          Sample View
        </li>
    </metal:block>

<body>
</html>
"""
    with open(os.path.join(views_path + '/view.pt'), 'w') as f:
        f.write(template)
    template = """<configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="collective.todo">

      -*- extra stuff goes here -*-
      <browser:page
         name="view"
         for="*"
         class=".view.MyView"
         template="view.pt"
         permission="zope2.View"
         />


    </configure>
    """
    with open(os.path.join(views_path + '/configure.zcml'), 'w') as f:
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

  <include package=".views" />

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
            'view_name': 'view',
            'view_python_class': True,
            'view_python_class_name': 'MyView',
            'view_template': True,
            'view_template_name': 'view',
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
    view.prepare_renderer(configurator)
    view.post_renderer(configurator)
