# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import remove_unwanted_files
from bobtemplates.plone.base import update_configure_zcml
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort
from lxml import etree

import case_conversion as cc


def get_service_name_from_python_class(configurator, question):
    """Get default service_name from python class"""
    class_name = configurator.variables["service_class_name"]
    if class_name:
        generated_name = cc.snakecase(class_name).replace("_", "-")
        question.default = generated_name
    else:
        question.default = "my-service"


def _update_package_configure_zcml(configurator):
    path = "{0}".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    match_xpath = "include[@package='.api']"
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".api" />
"""
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _update_api_configure_zcml(configurator):
    path = "{0}/api".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    example_file_name = "{0}.example".format(file_name)
    match_xpath = "zope:include[@package='.services']"
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".services" />
"""
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        example_file_name=example_file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _update_services_configure_zcml(configurator):
    path = "{0}/api/services".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    example_file_name = "{0}.example".format(file_name)
    match_xpath = "zope:include[@package='.{0}']".format(
        configurator.variables["service_class_name_normalized"],
    )
    match_str = "-*- extra stuff goes here -*-"
    insert_str = '<include package=".{0}" />\n'.format(
        configurator.variables["service_class_name_normalized"],
    )
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        example_file_name=example_file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _update_metadata_xml(configurator):
    """Add plone.restapi dependency metadata.xml in
    Generic Setup profiles.
    """
    metadata_file_name = "metadata.xml"
    metadata_file_dir = "profiles/default"
    metadata_file_path = (
        configurator.variables["package_folder"]
        + "/"
        + metadata_file_dir
        + "/"
        + metadata_file_name
    )

    with open(metadata_file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        dependencies = tree.xpath("/metadata/dependencies")[0]
        dep = "profile-plone.restapi:default"
        dep_exists = False
        for e in dependencies.iter("dependency"):
            dep_name = e.text
            if dep_name == dep:
                dep_exists = True

        if dep_exists:
            print(
                "{dep} already in metadata.xml, skip adding!".format(
                    dep=dep,
                ),
            )
            return
        dep_element = etree.Element("dependency")
        dep_element.text = dep
        dependencies.append(dep_element)

    with open(metadata_file_path, "wb") as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )


def _remove_unwanted_files(configurator):
    file_paths = []
    rel_file_paths = [
        "/api/configure.zcml.example",
        "/api/services/configure.zcml.example",
    ]
    base_path = configurator.variables["package_folder"]
    for rel_file_path in rel_file_paths:
        file_paths.append("{0}{1}".format(base_path, rel_file_path))
    remove_unwanted_files(file_paths)


def pre_renderer(configurator):
    """Pre rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "restapi_service"
    name = configurator.variables["service_name"].strip("_")
    name_normalized = cc.snakecase(name)
    configurator.variables["service_name_normalized"] = name_normalized
    class_name = configurator.variables["service_class_name"].strip("_")  # NOQA: E501
    configurator.variables["service_class_name"] = cc.pascalcase(  # NOQA: E501
        class_name,
    )
    configurator.variables["service_class_name_normalized"] = cc.snakecase(
        class_name,
    )
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_package_configure_zcml(configurator)
    _update_api_configure_zcml(configurator)
    _update_services_configure_zcml(configurator)
    _update_metadata_xml(configurator)
    _remove_unwanted_files(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add restapi_service: {0}".format(
            configurator.variables["service_name"],
        ),
    )
