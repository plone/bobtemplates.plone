# -*- coding: utf-8 -*-
"""Generate view."""

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import CONTENT_TYPE_INTERFACES
from bobtemplates.plone.base import echo
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree
from mrbob.bobexceptions import SkipQuestion
from mrbob.bobexceptions import ValidationError

import case_conversion as cc
import os
import six


def _view_name_from_python_class(configurator):
    view_generated_name = ""
    if configurator.variables["view_python_class"]:
        view_class_name = configurator.variables["view_python_class_name"]
        view_generated_name = cc.snakecase(view_class_name).replace("_", "-")
    return view_generated_name


def get_view_name_from_python_class(configurator, question):
    """Generate view default name from python class"""
    if configurator.variables["view_python_class"]:
        view_generated_name = _view_name_from_python_class(configurator)
        question.default = view_generated_name
    else:
        question.default = "my_view"


def get_view_template_name_from_python_class(configurator, question):
    if configurator.variables["view_python_class"]:
        view_class_name = configurator.variables["view_python_class_name"]
        view_generated_name = cc.snakecase(view_class_name)  # NOQA: E501
        question.default = view_generated_name
    else:
        question.default = "my_view"


def check_python_class_answer(configurator, question):
    if not configurator.variables["view_python_class"]:
        raise SkipQuestion(
            "No python class, so we skip python class name question."
        )  # NOQA: E501


def check_view_template_answer(configurator, question):
    if (
        not configurator.variables["view_template"]
        and not configurator.variables["view_python_class"]
    ):  # NOQA: E501
        raise ValidationError(
            "View must at least have a template or a python class"
        )  # NOQA: E501
    elif not configurator.variables["view_template"]:
        raise SkipQuestion(
            "No view template, so we skip view template name question."
        )  # NOQA: E501


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
    if configurator.variables["view_template"]:
        config["template"] = "{0}.pt".format(
            configurator.variables["view_template_name"]
        )
    if configurator.variables["view_python_class"]:
        config["class"] = ".{0}.{1}".format(
            configurator.variables["view_python_file_name"],
            configurator.variables["view_python_class_name"],
        )
    # if configurator.variables["view_permission"]:
    config["permission"] = "zope2.View"
    return config


def _update_views_configure_zcml(configurator):
    file_name = "configure.zcml"
    directory_path = configurator.variables["package_folder"] + "/views/"
    file_path = directory_path + file_name
    configure_example_file_path = (
        configurator.variables["package_folder"] + "/views/configure.zcml.example"
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
    if "template" in view_config:
        insert_str += '    template="{0}"\n'.format(view_config["template"])
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
        view_name_xpath = "./browser:page[@name='{0}']".format(
            view_config["name"],
        )
        view_for_xpath = "./browser:page[@for='{0}']".format(
            view_config["for"],
        )
        if len(tree_root.xpath(view_name_xpath, namespaces=ZCML_NAMESPACES)) and len(
            tree_root.xpath(view_for_xpath, namespaces=ZCML_NAMESPACES)
        ):
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
        view_xpath = "{0}include[@package='.views']".format(namespaces)
        if len(tree_root.findall(view_xpath)):
            print(
                ".views already in configure.zcml, skip adding!",
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".views" />
"""
    update_file(configurator, file_path, match_str, insert_str)


def _delete_unwanted_files(configurator):
    directory_path = configurator.variables["package_folder"] + "/views/"
    if not configurator.variables["view_template"]:
        file_name = "{0}.pt".format(
            configurator.variables["view_template_name"],
        )
        file_path = directory_path + file_name
        os.remove(file_path)

    elif not configurator.variables["view_python_class"]:
        file_name = "{0}.py".format(
            configurator.variables["view_python_file_name"],
        )
        file_path = directory_path + file_name
        os.remove(file_path)

    file_name = "configure.zcml.example"
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name in file_list:
        file_path = directory_path + file_name
        os.remove(file_path)


def prepare_renderer(configurator):
    """Prepare rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "view"
    view_name = configurator.variables["view_name"].strip("_")
    normalized_view_name = cc.snakecase(view_name)
    configurator.variables["view_name_normalized"] = normalized_view_name
    if configurator.variables["view_python_class"]:
        python_class_name = configurator.variables["view_python_class_name"].strip(
            "_"
        )  # NOQA: E501
        configurator.variables["view_python_class_name"] = cc.pascalcase(  # NOQA: E501
            python_class_name,
        )
        view_python_file_name = cc.snakecase(python_class_name)
        configurator.variables["view_python_file_name"] = view_python_file_name
        view_name_from_input = normalized_view_name.replace("_", "-")
        view_name_from_python_class = view_python_file_name.replace("_", "-")
        if view_name_from_input != view_name_from_python_class:
            configurator.variables["view_name"] = view_name_from_input
    else:
        configurator.variables["view_python_file_name"] = normalized_view_name

    if not configurator.variables["view_template"]:
        configurator.variables["view_template_name"] = normalized_view_name

    if not configurator.variables.get("view_base_class"):
        configurator.variables["view_base_class"] = "BrowserView"

    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_configure_zcml(configurator)
    _update_views_configure_zcml(configurator)
    _delete_unwanted_files(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add view: {0}".format(
            configurator.variables["view_name"],
        ),
    )
