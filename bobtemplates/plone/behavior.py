# -*- coding: utf-8 -*-
from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import echo
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree

import case_conversion as cc
import os


def _update_package_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    nsprefix = "{http://namespaces.zope.org/zope}"

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = ".behaviors"
        xpath_selector = ".//{0}include[@package='{1}']".format(
            nsprefix,
            permid,
        )  # NOQA: S100
        if len(tree_root.findall(xpath_selector)):
            print("{0} already in configure.zcml, skip adding!".format(permid))
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <include package=".behaviors" />

"""
    update_file(configurator, file_path, match_str, insert_str)


def _update_behaviors_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/behaviors/" + file_name
    example_file_path = file_path + ".example"
    file_list = os.listdir(os.path.dirname(file_path))
    if file_name not in file_list:
        os.rename(example_file_path, file_path)

    namespaces = {"plone": "http://namespaces.plone.org/plone"}
    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        behavior_name = "{0}.{1}".format(
            configurator.variables["behavior_name_normalized"],
            configurator.variables["behavior_name_klass"],
        )
        xpath_str = "./plone:behavior[@factory='{0}']".format(behavior_name)
        if len(tree_root.xpath(xpath_str, namespaces=namespaces)):
            print(
                "{name} already in configure.zcml, skip adding!".format(
                    name=behavior_name,
                ),
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <plone:behavior
        name="{package_dottedname}.{normalized_name}"
        title="{title}"
        description="{description}"
        provides=".{normalized_name}.I{klass_name}"
        factory=".{normalized_name}.{klass_name}"
        marker=".{normalized_name}.I{klass_name}Marker"
        />

""".format(
        title=configurator.variables["behavior_name_klass"],
        description=configurator.variables["behavior_description"],
        normalized_name=configurator.variables["behavior_name_normalized"],
        klass_name=configurator.variables["behavior_name_klass"],
        package_dottedname=configurator.variables["package.dottedname"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "behavior"
    behavior_name = configurator.variables["behavior_name"].strip("_")
    configurator.variables["behavior_name_klass"] = cc.pascalcase(behavior_name)
    configurator.variables["behavior_name_normalized"] = cc.snakecase(  # NOQA: E501
        behavior_name
    )
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """ """
    _update_package_configure_zcml(configurator)
    _update_behaviors_configure_zcml(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add behavior: {0}".format(
            configurator.variables["behavior_name"],
        ),
    )
    behavior_name = "{0}.behaviors.{1}.{2}".format(
        configurator.variables["package.dottedname"],
        configurator.variables["behavior_name_normalized"],
        configurator.variables["behavior_name_klass"],
    )
    behavior_name_short = "{0}.{1}".format(
        configurator.variables["package.dottedname"],
        configurator.variables["behavior_name_normalized"],
    )
    echo(
        "===================================================\n"
        "=> Sucessfully added: {0} template.  \\o/ \n\n".format(
            configurator.variables["template_id"],
        ),
        "info",
    )
    echo(
        'You can lookup your behavior by the name:\n "{0}"\n'
        'or by the shorter version:\n "{1}"\n'.format(
            behavior_name,
            behavior_name_short,
        ),
        "info",
    )
