# -*- coding: utf-8 -*-
"""Generate form."""

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import CONTENT_TYPE_INTERFACES
from bobtemplates.plone.base import echo
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree

import case_conversion as cc
import os
import six


# from mrbob.bobexceptions import SkipQuestion, ValidationError


def get_form_name_from_python_class(configurator, question):
    """Generate form default name from python class"""
    form_class_name = configurator.variables["form_python_class_name"]
    form_generated_name = cc.snakecase(form_class_name).replace("_", "-")  # NOQA: E501
    question.default = form_generated_name


def get_form_configuration(configurator):
    """return a dict with form configuration used for registration in zcml"""
    config = dict()
    config["name"] = configurator.variables["form_name"]
    # get Interface by content type or use the string it self as interface
    config["for"] = "{0}".format(
        CONTENT_TYPE_INTERFACES.get(
            configurator.variables["form_register_for"],
            configurator.variables["form_register_for"],
        )
    )
    config["class"] = ".{0}.{1}".format(
        configurator.variables["form_python_file_name"],
        configurator.variables["form_python_class_name"],
    )
    # if configurator.variables["form_permission"]:
    config["permission"] = "cmf.ManagePortal"
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

    form_config = get_form_configuration(configurator)
    insert_str = """
  <browser:page
    name="{0}"
    for="{1}"
""".format(
        form_config["name"],
        form_config["for"],
    )
    if "class" in form_config:
        insert_str += '    class="{0}"\n'.format(form_config["class"])
    # if "template" in form_config:
    #     insert_str += '    template="{0}"\n'.format(form_config["template"])
    if "permission" in form_config:
        insert_str += '    permission="{0}"\n'.format(form_config["permission"])
    insert_str += '    layer="{0}.interfaces.I{1}"\n'.format(
        configurator.variables["package.dottedname"],
        configurator.variables["package.browserlayer"],
    )
    insert_str += "    />\n"

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        form_xpath = "./browser:page[@name='{0}']".format(
            configurator.variables["form_name"],
        )
        if len(tree_root.xpath(form_xpath, namespaces=ZCML_NAMESPACES)):
            echo(
                "{0} already in configure.zcml, do you really want to add this config?"
                "\n\n{1}\n [y/N]: ".format(
                    configurator.variables["form_name"],
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
        form_xpath = "{0}include[@package='.forms']".format(namespaces)
        if len(tree_root.findall(form_xpath)):
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
    form_name = configurator.variables["form_name"].strip("_")
    normalized_form_name = cc.snakecase(form_name)
    configurator.variables["form_name_normalized"] = normalized_form_name
    python_class_name = configurator.variables["form_python_class_name"].strip("_")
    configurator.variables["form_python_class_name"] = cc.pascalcase(  # NOQA: E501
        python_class_name,
    )
    form_python_file_name = cc.snakecase(python_class_name)
    configurator.variables["form_python_file_name"] = form_python_file_name
    form_name_from_input = normalized_form_name.replace("_", "-")
    form_name_from_python_class = form_python_file_name.replace("_", "-")
    if form_name_from_input != form_name_from_python_class:
        configurator.variables["form_name"] = form_name_from_input

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
            configurator.variables["form_name"],
        ),
    )
