from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import echo
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree
from mrbob.configurator import maybe_bool

import case_conversion as cc
import os


def _update_package_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = ".vocabularies"
        xpath_selector = f"./include[@package='{permid}']"
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(f"{permid} already in configure.zcml, skip adding!")
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <include package=".vocabularies" />

"""
    update_file(configurator, file_path, match_str, insert_str)


def _update_vocabularies_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/vocabularies/" + file_name
    example_file_path = file_path + ".example"
    file_list = os.listdir(os.path.dirname(file_path))
    if file_name not in file_list:
        os.rename(example_file_path, file_path)

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        vocab_name = (
            f"{configurator.variables['package.dottedname']}"
            f".{configurator.variables['vocabulary_name_klass']}"
        )
        xpath_selector = f"./utility[@name='{vocab_name}']"
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
            print(f"{vocab_name} already in configure.zcml, skip adding!")
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <utility
        component=".{0}.{1}Factory"
        name="{2}.{1}"
    />

""".format(
        configurator.variables["vocabulary_name_normalized"],
        configurator.variables["vocabulary_name_klass"],
        configurator.variables["package.dottedname"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "vocabulary"
    vocabulary_name = configurator.variables["vocabulary_name"].strip("_")
    configurator.variables["vocabulary_name_klass"] = cc.pascalcase(vocabulary_name)
    configurator.variables["vocabulary_name_normalized"] = cc.snakecase(vocabulary_name)
    configurator.target_directory = configurator.variables["package_folder"]
    is_static_catalog_vocab = configurator.variables.get("is_static_catalog_vocab")
    if is_static_catalog_vocab:
        configurator.variables["is_static_catalog_vocab"] = maybe_bool(
            configurator.variables["is_static_catalog_vocab"]
        )


def post_renderer(configurator):
    """"""
    _update_package_configure_zcml(configurator)
    _update_vocabularies_configure_zcml(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator, f"Add vocabulary: {configurator.variables['vocabulary_name']}"
    )
    registered_vocabulary = (
        f"{configurator.variables['package.dottedname']}"
        f".{configurator.variables['vocabulary_name_klass']}"
    )
    echo(
        f"------------------------\n"
        f"Sucessfully added: {configurator.variables['template_id']} template.\n"
    )
    echo(
        f"You can lookup your vocabulary by the name: {registered_vocabulary}\n",
        "info",
    )
