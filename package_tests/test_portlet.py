# -*- coding: utf-8 -*-

"""Test view generation."""

from bobtemplates.plone import base
from bobtemplates.plone import portlet
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import os
import pytest


def test_pre_renderer():
    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory=".",
        variables={
            "portlet_name": "My nice portlet, with umlauts: öÖÖÖÖ".encode(
                "utf8",
            ),
        },
    )
    portlet.prepare_renderer(configurator)
    expt = "my_nice_portlet_with_umlauts_ooooo"
    assert configurator.variables["portlet_name_normalized"] == expt


def test_update_configure_zcml_with_changes(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.demo"
    package_path = target_path + "/src/collective/demo"
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

  <include package=".portlets" />

  <include package=".browser" />

</configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory="collective.demo",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "package_folder": package_path,
        },
    )
    portlet._update_configure_zcml(configurator)

    with open(os.path.join(package_path + "/configure.zcml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_configure_zcml_without_changes(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.demo"
    package_path = target_path + "/src/collective/demo"
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
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory="collective.demo",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "package_folder": package_path,
        },
    )
    portlet._update_configure_zcml(configurator)

    complete_template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.demo">

  <i18n:registerTranslations directory="locales" />

  <!--<includeDependencies package="." />-->

  <include package=".portlets" />

  <include package=".browser" />

</configure>
"""

    with open(os.path.join(package_path + "/configure.zcml"), "r") as f:
        content = f.read()
        if content != complete_template:
            pytest.raises(ValidationError)


def test_update_portlets_configure_zcml(tmpdir):
    """Test configure changes when changes are already in place."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    portlets_path = package_path + "/portlets/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(portlets_path)
    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.sample">

  '-*- extra stuff goes here -*-'

  <plone:portlet
    name="collective.sample.portlets.MyWeather"
    interface=".my_weather.IMyWeatherPortlet"
    assignment=".my_weather.Assignment"
    renderer=".my_weather.Renderer"
    addview=".my_weather.AddForm"
    editview=".my_weather.EditForm" />

</configure>
"""
    with open(os.path.join(portlets_path + "configure.zcml"), "w") as f:
        f.write(template)
    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "portlet_name": "MyWeather",
            "portlet_name_normalized": "my_weather",
            "portlet_configuration_name": "collective.sample.portlets.MyWeather",  # NOQA: E501
            "data_provider_class_name": "IMyWeatherPortlet",
            "package_folder": package_path,
            "package.dottedname": "collective.sample",
        },
    )
    portlet._update_portlets_configure_zcml(configurator)

    with open(os.path.join(portlets_path + "configure.zcml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_delete_unnecessary_files(tmpdir):
    """Test to remove unwanted file."""
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    portlets_path = package_path + "/portlets/"
    profile_path = package_path + "/profiles/default/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(portlets_path)
    os.makedirs(profile_path)
    file_name = "configure.zcml.example"
    portlets_file_path = portlets_path + file_name
    open(portlets_file_path, "a").close()
    file_name = "portlets.xml.example"
    xml_file_path = profile_path + file_name
    open(xml_file_path, "a").close()
    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "package_folder": package_path,
        },
    )
    portlet._delete_unnecessary_files(configurator)
    if os.path.isfile(portlets_file_path):
        pytest.raises(ValidationError)
    if os.path.isfile(xml_file_path):
        pytest.raises(ValidationError)


def test_update_portlets_xml(tmpdir):
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    profile_path = package_path + "/profiles/default/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profile_path)
    template = """<?xml version="1.0"?>
<portlets
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="plone">
  <!-- Extra portlets here  -->


</portlets>"""
    with open(os.path.join(profile_path + "portlets.xml.example"), "w") as f:
        f.write(template)

    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "portlet_name": "My Weather",
            "portlet_name_normalized": "my_weather",
            "portlet_configuration_name": "collective.sample.portlets.MyWeather",  # NOQA: E501
            "package_folder": package_path,
        },
    )
    portlet._update_portlets_xml(configurator)

    template = """<?xml version="1.0"?>
<portlets
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="plone">
  <!-- Extra portlets here  -->

  <portlet
    addview="collective.sample.portlets.MyWeather"
    title="My Weather"
    description="A portlet which can render weather of the given place."
    i18n:attributes="title title_my_weather;
                     description description_my_weather">

    <!-- This will enable the portlet for right column,
    left column and the footer too.
    -->
    <for interface="plone.app.portlets.interfaces.IColumn" />

    <!--
    This will enable the portlet in the dashboard.
    -->
    <!--<for interface="plone.app.portlets.interfaces.IDashboard" />-->

  </portlet>


</portlets>"""

    with open(os.path.join(profile_path + "portlets.xml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_update_portlets_xml_with_changes(tmpdir):
    target_path = tmpdir.strpath + "/collective.sample"
    package_path = target_path + "/src/collective/sample"
    profile_path = package_path + "/profiles/default/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(profile_path)
    template = """<?xml version="1.0"?>
<portlets
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="plone">
  <!-- Extra portlets here  -->

  <portlet
    addview="collective.sample.portlets.MyWeather"
    title="My Weather"
    description="A portlet which can render weather of the given place."
    i18n:attributes="title title_my_weather;
                     description description_my_weather">

    <!-- This will enable the portlet for right column,
    left column and the footer too.
    -->
    <for interface="plone.app.portlets.interfaces.IColumn" />

    <!--
    This will enable the portlet in the dashboard.
    -->
    <!--<for interface="plone.app.portlets.interfaces.IDashboard" />-->

  </portlet>

</portlets>"""

    with open(os.path.join(profile_path + "portlets.xml.example"), "w") as f:
        f.write(template)

    configurator = Configurator(
        template="bobtemplates.plone:portlet",
        target_directory="collective.sample",
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "portlet_name": "My Weather",
            "portlet_name_normalized": "my_weather",
            "portlet_configuration_name": "collective.sample.portlets.MyWeather",  # NOQA: E501
            "package_folder": package_path,
        },
    )
    portlet._update_portlets_xml(configurator)

    with open(os.path.join(profile_path + "portlets.xml"), "r") as f:
        content = f.read()
        if content != template:
            pytest.raises(ValidationError)


def test_post_renderer(tmpdir):
    """Test post rendering."""
    target_path = tmpdir.strpath + "/collective.todo"
    package_path = target_path + "/src/collective/todo"
    portlets_path = package_path + "/portlets"
    profile_path = package_path + "/profiles/default/"
    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(portlets_path)
    os.makedirs(profile_path)

    template = """# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.todo import _
from plone import schema
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer

import json
import urllib
import urllib2


class IMyWeatherPortlet(IPortletDataProvider):
    place_str = schema.TextLine(
        title=_(u'Name of your place with country code'),
        description=_(u'City name along with country code i.e Delhi,IN'),  # NOQA: E501
        required=True,
        default=u'delhi,in'
    )


@implementer(IMyWeatherPortlet)
class Assignment(base.Assignment):
    schema = IMyWeatherPortlet

    def __init__(self, place_str='delhi,in'):
        self.place_str = place_str.lower()

    @property
    def title(self):
        return _(u'Weather of the place')


class AddForm(base.AddForm):
    schema = IMyWeatherPortlet
    form_fields = field.Fields(IMyWeatherPortlet)
    label = _(u'Add Place weather')
    description = _(u'This portlet displays weather of the place.')

    def create(self, data):
        return Assignment(
            place_str=data.get('place_str', 'delhi,in'),
        )


class EditForm(base.EditForm):
    schema = IMyWeatherPortlet
    form_fields = field.Fields(IMyWeatherPortlet)
    label = _(u'Edit Place weather')
    description = _(u'This portlet displays weather of the place.')


class Renderer(base.Renderer):
    schema = IMyWeatherPortlet
    _template = ViewPageTemplateFile('my_weather.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request),
            name=u'plone_portal_state'
        )
        self.anonymous = portal_state.anonymous()

    def render(self):
        return self._template()

    @property
    def available(self):
        \"""Show the portlet only if there are one or more elements.\"""
        return not self.anonymous and self._data()

    def weather_report(self):
        self.result = self._data()
        return self.result['description']

    def get_humidity(self):
        return self.result['humidity']

    def get_pressure(self):
        return self.result['pressure']
"""
    with open(os.path.join(portlets_path + "/my_weather.py"), "w") as f:
        f.write(template)

    template = """<div class="weather">
    <h3>Weather Report</h3>
    ${view/weather_report}
    <br>
    Pressure: ${view/get_pressure}
    <br>
    Humidity: ${view/get_humidity}
    <br>
</div>
"""
    with open(os.path.join(portlets_path + "/my_weather.pt"), "w") as f:
        f.write(template)
    template = """<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:browser="http://namespaces.zope.org/browser"
  xmlns:plone="http://namespaces.plone.org/plone">

  <include package="plone.app.portlets" />

  '-*- extra stuff goes here -*-'

  <plone:portlet
    name="collective.todo.portlets.MyWeather"
    interface=".my_weather.IMyWeatherPortlet"
    assignment=".my_weather.Assignment"
    renderer=".my_weather.Renderer"
    addview=".my_weather.AddForm"
    editview=".my_weather.EditForm" />

</configure>"""
    with open(os.path.join(portlets_path + "/configure.zcml"), "w") as f:
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

  <include package=".portlets" />

</configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)

    template = """
        dummy
        '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + "/setup.py"), "w") as f:
        f.write(template)

    template = """<?xml version="1.0"?>
<portlets
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="plone">
  <!-- Extra portlets here  -->

  <portlet
    addview="collective.todo.portlets.MyWeather"
    title="My Weather"
    description="A portlet which can render weather of the given place."
    i18n:attributes="title title_my_weather;
                     description description_my_weather">

    <!-- This will enable the portlet for right column,
    left column and the footer too.
    -->
    <for interface="plone.app.portlets.interfaces.IColumn" />

    <!--
    This will enable the portlet in the dashboard.
    -->
    <!--<for interface="plone.app.portlets.interfaces.IDashboard" />-->

  </portlet>


</portlets>
"""
    with open(os.path.join(profile_path + "/portlets.xml.example"), "w") as f:
        f.write(template)

    configurator = Configurator(
        template="bobtemplates.plone:addon",
        target_directory=package_path,
        bobconfig={
            "non_interactive": True,
        },
        variables={
            "portlet_name": "My Weather",
            "plone.version": "5.1",
        },
    )
    os.chdir(package_path)
    base.set_global_vars(configurator)
    portlet.prepare_renderer(configurator)
    portlet.post_renderer(configurator)
