from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import echo
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from lxml import etree
from mrbob.bobexceptions import ValidationError

import case_conversion as cc
import re


def check_name(configurator, question, answer):
    if not re.match("^[a-z]+-+[a-z0-9]+(-+[a-z0-9]+)*$", answer):
        raise ValidationError(
            f"{answer} is not a valid custom-element identifier."
            f" Please try something like this 'my-element'"
        )
    return answer


def _update_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    namespaces = {"plone": "http://namespaces.plone.org/plone"}

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()

        xpath = (
            f"./plone:static[@name='{configurator.variables['package.dottedname']}"
            ".svelte']"
        )
        if len(tree_root.xpath(xpath, namespaces=namespaces)):
            print(
                f"{configurator.variables['package.dottedname']}.svelte "
                "already in configure.zcml, skip adding!"
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = f"""
  <plone:static
      xmlns:plone="http://namespaces.plone.org/plone"
      directory="svelte_apps"
      type="plone"
      name="{configurator.variables["package.dottedname"]}.svelte"
      />

"""
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
    git_commit(
        configurator,
        f"Add Svelte app: in svelte_apps/{configurator.variables['svelte_app_name']}",
    )
    echo(
        "===================================================\n"
        f"=> Sucessfully added: {configurator.variables['template_id']} "
        f"in svelte_apps/{configurator.variables['svelte_app_name']} \n"
        "=> you might want to go into the dir and run:\n"
        "$ yarn\n"
        "and then:"
        "$ yarn dev\n",
        "info",
    )
