# -*- coding: utf-8 -*-
"""Generate form."""

import os

import case_conversion as cc
import six
from lxml import etree
# from mrbob.bobexceptions import SkipQuestion, ValidationError

from bobtemplates.plone.base import (
    CONTENT_TYPE_INTERFACES,
    ZCML_NAMESPACES,
    base_prepare_renderer,
    echo,
    git_commit,
    update_file,
)
from bobtemplates.plone.utils import run_black, run_isort

from pprint import pprint


def get_view_name_from_python_class(configurator, question):
    """Generate view default name from python class"""
    view_class_name = configurator.variables["view_python_class_name"]
    view_generated_name = cc.snakecase(view_class_name).replace("_", "-")  # NOQA: E501
    question.default = view_generated_name


def get_view_configuration(configurator):
    """return a dict with view configuration used for registration in zcml"""
    config = dict()
    config["name"] = configurator.variables["view_name"]
    # get Interface by content type or use the string it self as interface
    config["for"] = "{0}".format(
        CONTENT_TYPE_INTERFACES.get(
            configurator.variables["view_register_for"],
            configurator.variables["view_register_for"],
        )
    )
    config["class"] = ".{0}.{1}".format(
        configurator.variables["view_python_file_name"],
        configurator.variables["view_python_class_name"],
    )
    # if configurator.variables["view_permission"]:
    config["permission"] = "zope2.View"
    return config


def _update_forms_configure_zcml(configurator):
    file_name = "configure.zcml"
    directory_path = configurator.variables["package_folder"] + "/forms/"
    file_path = directory_path + file_name
    configure_example_file_path = (
        configurator.variables["package_folder"] + "/forms/configure.zcml.example"
    )
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name not in file_list:
        os.rename(configure_example_file_path, file_path)

    match_str = "-*- extra stuff goes here -*-"

    view_config = get_view_configuration(configurator)
    insert_str = """
  <browser:page
    name="{0}"
    for="{1}"
""".format(
        view_config["name"],
        view_config["for"],
    )
    if "class" in view_config:
        insert_str += '    class="{0}"\n'.format(view_config["class"])
    # if "template" in view_config:
    #     insert_str += '    template="{0}"\n'.format(view_config["template"])
    if "permission" in view_config:
        insert_str += '    permission="{0}"\n'.format(view_config["permission"])
    insert_str += '    layer="{0}.interfaces.I{1}"\n'.format(
        configurator.variables["package.dottedname"],
        configurator.variables["package.browserlayer"],
    )
    insert_str += "    />\n"

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        view_xpath = "./browser:page[@name='{0}']".format(
            configurator.variables["view_name"],
        )
        if len(tree_root.xpath(view_xpath, namespaces=ZCML_NAMESPACES)):
            echo(
                "{0} already in configure.zcml, do you really want to add this config?"
                "\n\n{1}\n [y/N]: ".format(
                    configurator.variables["view_name"],
                    insert_str,
                ),
                "info",
            )
            if configurator.bobconfig.get("non_interactive"):
                return
            choice = six.moves.input().lower()
            if choice != "y":
                return

    update_file(configurator, file_path, match_str, insert_str)


def _update_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    namespaces = "{http://namespaces.zope.org/zope}"

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        view_xpath = "{0}include[@package='.forms']".format(namespaces)
        if len(tree_root.findall(view_xpath)):
            print(
                ".forms already in configure.zcml, skip adding!",
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".forms" />
"""
    update_file(configurator, file_path, match_str, insert_str)


def _delete_unwanted_files(configurator):
    directory_path = configurator.variables["package_folder"] + "/forms/"

    file_name = "configure.zcml.example"
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name in file_list:
        file_path = directory_path + file_name
        os.remove(file_path)


def prepare_renderer(configurator):
    """Prepare rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "form"
    view_name = configurator.variables["view_name"].strip("_")
    normalized_view_name = cc.snakecase(view_name)
    configurator.variables["view_name_normalized"] = normalized_view_name
    python_class_name = configurator.variables["view_python_class_name"].strip("_")
    configurator.variables["view_python_class_name"] = cc.pascalcase(  # NOQA: E501
        python_class_name,
    )
    view_python_file_name = cc.snakecase(python_class_name)
    configurator.variables["view_python_file_name"] = view_python_file_name
    view_name_from_input = normalized_view_name.replace("_", "-")
    view_name_from_python_class = view_python_file_name.replace("_", "-")
    if view_name_from_input != view_name_from_python_class:
        configurator.variables["view_name"] = view_name_from_input

    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_configure_zcml(configurator)
    _update_forms_configure_zcml(configurator)
    _delete_unwanted_files(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add form: {0}".format(
            configurator.variables["view_name"],
        ),
    )
