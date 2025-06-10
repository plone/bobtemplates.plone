"""Generate view."""

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import ZCML_NAMESPACES
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree
from mrbob.bobexceptions import SkipQuestion

import case_conversion as cc
import os


def get_view_name_from_python_class(configurator, question):
    """Generate view default name from python class"""
    view_class_name = configurator.variables["viewlet_python_class_name"]
    view_generated_name = cc.snakecase(view_class_name).replace("_", "-")
    question.default = view_generated_name


def check_viewlet_template_answer(configurator, question):
    if not configurator.variables["viewlet_template"]:
        raise SkipQuestion("No view template, so we skip view template name question.")


def _update_configure_zcml(configurator):
    file_name = "configure.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    namespaces = "{http://namespaces.zope.org/zope}"

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        view_xpath = f"{namespaces}include[@package='.viewlets']"
        if len(tree_root.findall(view_xpath)):
            print(
                ".viewlets already in configure.zcml, skip adding!",
            )
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".viewlets" />
"""
    update_file(configurator, file_path, match_str, insert_str)


def _update_viewlets_configure_zcml(configurator):
    file_name = "configure.zcml"
    directory_path = configurator.variables["package_folder"] + "/viewlets/"
    file_path = directory_path + file_name

    configure_example_file_path = (
        configurator.variables["package_folder"] + "/viewlets/configure.zcml.example"
    )
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name not in file_list:
        os.rename(configure_example_file_path, file_path)

    with open(file_path) as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        view_xpath = (
            f"./browser:viewlet[@name='{configurator.variables['viewlet_name']}']"
        )
        if len(tree_root.xpath(view_xpath, namespaces=ZCML_NAMESPACES)):
            print(
                f"{configurator.variables['viewlet_name']}"
                f" already in configure.zcml, skip adding!!!"
            )
            return

    match_str = "-*- extra stuff goes here -*-"

    iface_name = "plone.app.contenttypes.interfaces.IDocument"

    if configurator.variables["viewlet_template"]:
        insert_str = f"""
  <browser:viewlet
     name="{configurator.variables["viewlet_name"]}"
     for="{iface_name}"
     manager="plone.app.layout.viewlets.interfaces.IAboveContentTitle"
     layer="{configurator.variables["package.dottedname"]}.interfaces.I{configurator.variables["package.browserlayer"]}"
     class=".{configurator.variables["viewlet_python_file_name"]}.{configurator.variables["viewlet_python_class_name"]}"
     template="{configurator.variables["viewlet_template_name"]}.pt"
     permission="zope2.View"
     />
"""
    else:
        insert_str = f"""
  <browser:viewlet
     name="{configurator.variables["viewlet_name"]}"
     for="{iface_name}"
     manager="plone.app.layout.viewlets.interfaces.IAboveContentTitle"
     layer="{configurator.variables["package.dottedname"]}.interfaces.I{configurator.variables["package.browserlayer"]}"
     class=".{configurator.variables["viewlet_python_file_name"]}.{configurator.variables["viewlet_python_class_name"]}"
     permission="zope2.View"
     />
"""
    update_file(configurator, file_path, match_str, insert_str)


def _delete_unwanted_files(configurator):
    directory_path = configurator.variables["package_folder"] + "/viewlets/"
    if not configurator.variables["viewlet_template"]:
        template_file_name = f"{configurator.variables['viewlet_template_name']}.pt"
        file_path = directory_path + template_file_name
        os.remove(file_path)

    file_name = "configure.zcml.example"
    file_list = os.listdir(os.path.dirname(directory_path))
    if file_name in file_list:
        file_path = directory_path + file_name
        os.remove(file_path)


def prepare_renderer(configurator):
    """Prepare rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "viewlet"
    viewlet_name = configurator.variables["viewlet_name"].strip("_")
    normalized_viewlet_name = cc.snakecase(viewlet_name)
    configurator.variables["viewlet_name_normalized"] = normalized_viewlet_name
    if not configurator.variables["viewlet_template"]:
        configurator.variables["viewlet_template_name"] = normalized_viewlet_name
    python_class_name = configurator.variables["viewlet_python_class_name"].strip("_")
    configurator.variables["viewlet_python_class_name"] = cc.pascalcase(
        python_class_name,
    )
    viewlet_python_file_name = cc.snakecase(viewlet_name)
    configurator.variables["viewlet_python_file_name"] = viewlet_python_file_name
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_configure_zcml(configurator)
    _update_viewlets_configure_zcml(configurator)
    _delete_unwanted_files(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(configurator, f"Add viewlet: {configurator.variables['viewlet_name']}")
