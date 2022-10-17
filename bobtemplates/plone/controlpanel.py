# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree

import case_conversion as cc
import os


def _update_package_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = ".controlpanels"
        xpath_selector = "./include[@package='{0}']".format(permid)  # NOQA: E501
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print("{0} already in configure.zcml, skip adding!".format(permid))
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <include package=".controlpanels" />

"""
    update_file(configurator, file_path, match_str, insert_str)


def _update_controlpanels_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/controlpanels/" + file_name
    example_file_path = file_path + ".example"
    file_list = os.listdir(os.path.dirname(file_path))
    if file_name not in file_list:
        os.rename(example_file_path, file_path)

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()

        xpath_selector = "./include[@package='{0}']".format(
            configurator.variables["controlpanel_name_normalized"],
        )
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(
                "{0} already in configure.zcml, skip adding!".format(
                    configurator.variables["controlpanel_name_normalized"]
                )
            )  # NOQA: E501
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <include
        package=".{0}"
    />

""".format(
        configurator.variables["controlpanel_name_normalized"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def _update_profile_controlpanel_xml(configurator):
    file_name = "controlpanel.xml"
    file_path = (
        configurator.variables["package_folder"] + "/profiles/default/" + file_name
    )
    example_file_path = file_path + ".example"
    file_list = os.listdir(os.path.dirname(file_path))
    if file_name not in file_list:
        os.rename(example_file_path, file_path)

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()

        xpath_selector = "./configlet[@action_id='{0}-controlpanel']".format(
            configurator.variables["controlpanel_name_normalized"],
        )
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(
                "{0} already in {1} skip adding!".format(
                    configurator.variables["controlpanel_name_normalized"],
                    file_name,
                )
            )  # NOQA: E501
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <configlet
      i18n:attributes="title"
      title="{0}"
      action_id="{1}-controlpanel"
      appId="{1}-controlpanel"
      category="Products"
      condition_expr=""
      icon_expr=""
      url_expr="string:${{portal_url}}/@@{1}-controlpanel"
      visible="True">
    <permission>Manage Portal</permission>
  </configlet>

""".format(
        configurator.variables["controlpanel_separated_name"],
        configurator.variables["controlpanel_name_normalized"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "controlpanel"
    controlpanel_name = configurator.variables["controlpanel_python_class_name"].strip(
        "_"
    )
    configurator.variables["controlpanel_name_klass"] = cc.pascalcase(controlpanel_name)
    configurator.variables["controlpanel_name_normalized"] = cc.snakecase(  # NOQA: E501
        controlpanel_name
    )
    configurator.variables["controlpanel_separated_name"] = cc.separate_words(
        controlpanel_name
    )
    configurator.target_directory = configurator.variables["package_folder"]

    # compute the browserlayer like the addon template does
    camelcasename = (
        configurator.variables["package.dottedname"]
        .replace(".", " ")
        .title()
        .replace(" ", "")
        .replace("_", "")
    )
    configurator.variables["package.browserlayer"] = "{0}Layer".format(camelcasename)


def post_renderer(configurator):
    """"""
    _update_package_configure_zcml(configurator)
    _update_controlpanels_configure_zcml(configurator)
    _update_profile_controlpanel_xml(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add Control Panel: {0}".format(
            configurator.variables["controlpanel_python_class_name"],
        ),
    )
