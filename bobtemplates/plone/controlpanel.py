from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.base import update_configure_with_package
from lxml import etree

import case_conversion as cc
import os


def _update_package_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    update_configure_with_package(configurator, file_path, "controlpanels")


def _update_controlpanels_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/controlpanels/" + file_name
    example_file_path = file_path + ".example"
    file_list = os.listdir(os.path.dirname(file_path))
    if file_name not in file_list:
        os.rename(example_file_path, file_path)

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()

        controlpanel_name_normalized = configurator.variables[
            "controlpanel_name_normalized"
        ]
        xpath_selector = f"./include[@package='{controlpanel_name_normalized}']"
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(
                f"{controlpanel_name_normalized} "
                "already in configure.zcml, skip adding!"
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = f"""
    <include
        package=".{controlpanel_name_normalized}"
    />

"""
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

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()

        xpath_selector = (
            f"./configlet[@action_id='{configurator.variables['controlpanel_name_normalized']}"
            "-controlpanel']"
        )
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(
                f"{configurator.variables['controlpanel_name_normalized']} "
                f"already in {file_name} skip adding!"
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = f"""
  <configlet
      i18n:attributes="title"
      title="{configurator.variables["controlpanel_separated_name"]}"
      action_id="{configurator.variables["controlpanel_name_normalized"]}-controlpanel"
      appId="{configurator.variables["controlpanel_name_normalized"]}-controlpanel"
      category="Products"
      condition_expr=""
      icon_expr=""
      url_expr="string:${{portal_url}}/@@{configurator.variables["controlpanel_name_normalized"]}-controlpanel"
      visible="True">
    <permission>Manage Portal</permission>
  </configlet>

"""
    update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "controlpanel"
    controlpanel_name = configurator.variables["controlpanel_python_class_name"].strip(
        "_"
    )
    configurator.variables["controlpanel_name_klass"] = cc.pascalcase(controlpanel_name)
    configurator.variables["controlpanel_name_normalized"] = cc.snakecase(
        controlpanel_name
    )
    configurator.variables["controlpanel_separated_name"] = cc.separate_words(
        controlpanel_name
    )
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """"""
    _update_package_configure_zcml(configurator)
    _update_controlpanels_configure_zcml(configurator)
    _update_profile_controlpanel_xml(configurator)
    git_commit(
        configurator,
        f"Add Control Panel: "
        f"{configurator.variables['controlpanel_python_class_name']}",
    )
