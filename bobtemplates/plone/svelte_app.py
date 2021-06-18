# -*- coding: utf-8 -*-

import re

import case_conversion as cc
from lxml import etree
from mrbob.bobexceptions import ValidationError

from bobtemplates.plone.base import base_prepare_renderer, echo, git_commit, update_file
from bobtemplates.plone.utils import run_black, run_isort


def check_name(configurator, question, answer):
    if not re.match("^[a-z]+-+[a-z0-9]+(-+[a-z0-9]+)*$", answer):
        raise ValidationError(
            u"{key} is not a valid custom-element identifier. Please try something like this 'my-element'".format(
                key=answer
            )
        )  # NOQA: E501
    return answer


def _update_configure_zcml(configurator):
    file_name = u"configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    namespaces = {"plone": "http://namespaces.plone.org/plone"}

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        xpath = "./plone:static[@name='{}.svelte']".format(
            configurator.variables["package.dottedname"]
        )
        if len(tree_root.xpath(xpath, namespaces=namespaces)):
            print(
                "{name}.svelte already in configure.zcml, skip adding!".format(
                    name=configurator.variables["package.dottedname"]
                )
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <plone:static
      directory="svelte_apps"
      type="plone"
      name="{0}.svelte"
      />

""".format(
        configurator.variables["package.dottedname"]
    )
    update_file(configurator, file_path, match_str, insert_str)


def pre_renderer(configurator):
    """Pre rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "svelte_app"
    name = configurator.variables["svelte_app_name"].strip("_")
    configurator.variables["svelte_app_file_name"] = cc.snakecase(name)
    configurator.variables["svelte_app_name_dashed"] = cc.dashcase(name)


def post_renderer(configurator):
    """Post rendering."""
    _update_configure_zcml(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add Svelte app: in svelte_apps/{0}".format(
            configurator.variables["svelte_app_name"],
        ),
    )
    echo(
        "===================================================\n"
        "=> Sucessfully added: {0} in svelte_apps/{1} \n"
        "=> you might want to go into the dir and run:\n"
        "$ yarn\n"
        "and then:"
        "$ yarn dev\n".format(
            configurator.variables["template_id"],
            configurator.variables["svelte_app_name"],
        ),
        "info",
    )
