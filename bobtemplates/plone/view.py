# -*- coding: utf-8 -*-
"""Generate view."""

import os

import case_conversion as cc
import six
from lxml import etree
from mrbob.bobexceptions import SkipQuestion, ValidationError

from bobtemplates.plone.base import (
    ZCML_NAMESPACES,
    base_prepare_renderer,
    echo,
    git_commit,
    update_file,
)
from bobtemplates.plone.utils import run_black, run_isort


def get_view_name_from_python_class(configurator, question):
    """Generate view default name from python class"""
    if configurator.variables["view_python_class"]:
        view_class_name = configurator.variables["view_python_class_name"]
        view_generated_name = cc.snakecase(view_class_name).replace(
            "_", "-"
        )  # NOQA: E501
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
            u"No python class, so we skip python class name question."
        )  # NOQA: E501


def check_view_template_answer(configurator, question):
    if (
        not configurator.variables["view_template"]
        and not configurator.variables["view_python_class"]
    ):  # NOQA: E501
        raise ValidationError(
            u"View must at least have a template or a python class"
        )  # NOQA: E501
    elif not configurator.variables["view_template"]:
        raise SkipQuestion(
            u"No view template, so we skip view template name question."
        )  # NOQA: E501


def _update_views_configure_zcml(configurator):
    file_name = u"configure.zcml"
    directory_path = configurator.variables["package_folder"] + "/views/"
    file_path = directory_path + file_name
    configure_example_file_path = (
        configurator.variables["package_folder"] + "/views/configure.zcml.example"
    )  # NOQA: E501
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name not in file_list:
        os.rename(configure_example_file_path, file_path)

    match_str = "-*- extra stuff goes here -*-"

    if (
        configurator.variables["view_template"]
        and configurator.variables["view_python_class"]
    ):  # NOQA: E501
        insert_str = """
  <browser:page
    name="{0}"
    for="Products.CMFCore.interfaces.IFolderish"
    class=".{1}.{2}"
    template="{3}.pt"
    permission="zope2.View"
    />
""".format(
            configurator.variables["view_name"],
            configurator.variables["view_python_file_name"],
            configurator.variables["view_python_class_name"],
            configurator.variables["view_template_name"],
        )

    if (
        configurator.variables["view_template"]
        and not configurator.variables["view_python_class"]
    ):  # NOQA: E501
        insert_str = """
  <browser:page
    name="{0}"
    for="Products.CMFCore.interfaces.IFolderish"
    template="{1}.pt"
    permission="zope2.View"
    />
""".format(
            configurator.variables["view_name"],
            configurator.variables["view_template_name"],
        )

    if (
        not configurator.variables["view_template"]
        and configurator.variables["view_python_class"]
    ):  # NOQA: E501
        insert_str = """
  <browser:page
    name="{0}"
    for="Products.CMFCore.interfaces.IFolderish"
    class=".{1}.{2}"
    permission="zope2.View"
    />
""".format(
            configurator.variables["view_name"],
            configurator.variables["view_python_file_name"],
            configurator.variables["view_python_class_name"],
        )
    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        view_xpath = "./browser:page[@name='{0}']".format(
            configurator.variables["view_name"],
        )
        if len(tree_root.xpath(view_xpath, namespaces=ZCML_NAMESPACES)):
            echo(
                u"{0} already in configure.zcml, do you really want to add this config?"
                u"\n\n{1}\n [y/N]: ".format(
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
    file_name = u"configure.zcml"
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
        file_name = u"{0}.pt".format(
            configurator.variables["view_template_name"],
        )
        file_path = directory_path + file_name
        os.remove(file_path)

    elif not configurator.variables["view_python_class"]:
        file_name = u"{0}.py".format(
            configurator.variables["view_python_file_name"],
        )
        file_path = directory_path + file_name
        os.remove(file_path)

    file_name = u"configure.zcml.example"
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
