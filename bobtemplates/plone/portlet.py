# -*- coding: utf-8 -*-
"""Generate portlet."""

from __future__ import absolute_import
from __future__ import print_function

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from bobtemplates.plone.utils import slugify
from lxml import etree

import case_conversion as cc
import os


def _update_portlets_configure_zcml(configurator):
    file_name = "configure.zcml"
    directory_path = configurator.variables["package_folder"] + "/portlets/"
    file_path = directory_path + file_name
    configure_example_file_path = (
        configurator.variables["package_folder"] + "/portlets/configure.zcml.example"
    )  # NOQA: E501
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name not in file_list:
        os.rename(configure_example_file_path, file_path)

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        portlet_xpath = "./plone:portlet[@name='{0}']".format(
            configurator.variables["portlet_name"],
        )
        if len(tree_root.xpath(portlet_xpath, namespaces=ZCML_NAMESPACES)):
            print(
                (
                    "{0} already in configure.zcml, skip adding!".format(
                        configurator.variables["portlet_name"],
                    ),
                )
            )
            return

    match_str = "-*- extra stuff goes here -*-"

    insert_str = """
  <plone:portlet
    name="{0}"
    interface=".{1}.{2}"
    assignment=".{3}.Assignment"
    renderer=".{4}.Renderer"
    addview=".{5}.AddForm"
    editview=".{6}.EditForm" />
    """.format(
        configurator.variables["portlet_configuration_name"],
        configurator.variables["portlet_name_normalized"],
        configurator.variables["data_provider_class_name"],
        configurator.variables["portlet_name_normalized"],
        configurator.variables["portlet_name_normalized"],
        configurator.variables["portlet_name_normalized"],
        configurator.variables["portlet_name_normalized"],
    )

    update_file(configurator, file_path, match_str, insert_str)


def _update_portlets_xml(configurator):
    file_name = "portlets.xml"
    directory_path = (
        configurator.variables["package_folder"] + "/profiles/default/"
    )  # NOQA: E501
    file_path = directory_path + file_name
    configure_example_file_path = (
        configurator.variables["package_folder"]
        + "/profiles/default/portlets.xml.example"
    )  # NOQA: E501
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name not in file_list:
        os.rename(configure_example_file_path, file_path)

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        xpath_selector = "./portlet[@addview='{0}']".format(
            configurator.variables["portlet_configuration_name"],
        )
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(
                (
                    "{0} already in portlets.xml, skip adding!".format(
                        configurator.variables["portlet_configuration_name"],
                    ),
                )
            )
            return

    match_str = "<!-- Extra portlets here  -->"

    insert_str = """
  <portlet
    addview="{0}"
    title="{1}"
    description="A portlet which can render weather of the given place."
    i18n:attributes="title title_{2};
                     description description_{3}">

    <!-- This will enable the portlet for right column,
    left column and the footer too.
    -->
    <for interface="plone.app.portlets.interfaces.IColumn" />

    <!--
    This will enable the portlet in the dashboard.
    -->
    <!--<for interface="plone.app.portlets.interfaces.IDashboard" />-->

  </portlet>
""".format(
        configurator.variables["portlet_configuration_name"],
        configurator.variables["portlet_name"],
        configurator.variables["portlet_name_normalized"],
        configurator.variables["portlet_name_normalized"],
    )

    update_file(configurator, file_path, match_str, insert_str)


def _delete_unnecessary_files(configurator):
    directory_path = configurator.variables["package_folder"]
    configure_path = directory_path + "/portlets/"
    file_name = "configure.zcml.example"
    file_list = os.listdir(os.path.dirname(configure_path))
    if file_name in file_list:
        file_path = configure_path + file_name
        os.remove(file_path)
    portlets_xml_path = directory_path + "/profiles/default/"
    file_name = "portlets.xml.example"
    file_list = os.listdir(os.path.dirname(portlets_xml_path))
    if file_name in file_list:
        file_path = portlets_xml_path + file_name
        os.remove(file_path)


def _update_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        xpath_selector = "./include[@package='{0}']".format(".portlets")  # NOQA: E501
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print((".views already in configure.zcml, skip adding!",))
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".portlets" />
"""
    update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    """Prepare rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "portlet"
    portlet_name = configurator.variables["portlet_name"]
    normalized_portlet_name = cc.snakecase(slugify(portlet_name))  # NOQA: E501
    configurator.variables["portlet_name_normalized"] = normalized_portlet_name
    portlet_config_name = cc.pascalcase(normalized_portlet_name)
    configurator.variables[
        "portlet_configuration_name"
    ] = "{0}.portlets.{1}".format(  # NOQA: E501
        configurator.variables["package.dottedname"],
        portlet_config_name,
    )
    configurator.variables["data_provider_class_name"] = "I{0}Portlet".format(
        portlet_config_name,
    )
    configurator.target_directory = configurator.variables["package_folder"]
    package_name = configurator.variables["package.dottedname"].replace(
        ".", "_"
    )  # NOQA: E501
    browser_layer = cc.pascalcase(package_name)
    configurator.variables["browser_layer"] = "I{0}Layer".format(
        browser_layer,
    )


def post_renderer(configurator):
    """Post rendering."""
    _update_configure_zcml(configurator)
    _update_portlets_configure_zcml(configurator)
    _update_portlets_xml(configurator)
    _delete_unnecessary_files(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add portlet: {0}".format(
            configurator.variables["portlet_name"],
        ),
    )
