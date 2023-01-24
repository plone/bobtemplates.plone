# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import remove_unwanted_files
from bobtemplates.plone.base import update_configure_zcml
from lxml import etree


def _update_package_configure_zcml(configurator):
    path = "{0}".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    match_xpath = "zope:include[@package='.upgrades']"
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".upgrades" />
"""
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _update_upgrades_configure_zcml(configurator):
    path = "{0}/upgrades".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    example_file_name = "{0}.example".format(file_name)
    zcml_package_name = configurator.variables["upgrade_step_dest_version"]
    match_xpath = "zope:include[@file='{0}.zcml']".format(zcml_package_name)
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include file="{0}.zcml" />
""".format(
        zcml_package_name
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


def _remove_unwanted_files(configurator):
    file_paths = []
    rel_file_paths = [
        "/upgrades/configure.zcml.example",
    ]
    base_path = configurator.variables["package_folder"]
    for rel_file_path in rel_file_paths:
        file_paths.append("{0}{1}".format(base_path, rel_file_path))
    remove_unwanted_files(file_paths)


def _read_source_version(configurator):
    base_path = configurator.variables["package_folder"]
    rel_file_path = "/profiles/default/metadata.xml"
    metadata_path = "{0}{1}".format(base_path, rel_file_path)
    with open(metadata_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        match_xpath = "version"
        match_result = tree_root.findall(match_xpath)
        if not match_result:
            raise RuntimeError("source version not found in metadata.xml!")
            return
        return int(match_result[0].text)


def _write_dest_version(configurator):
    """Add plone.app.dexterity dependency metadata.xml in Generic Setup profiles."""  # NOQA: E501
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
        version = tree.xpath("/metadata/version")[0]
        version.text = str(configurator.variables["upgrade_step_dest_version"])

    with open(metadata_file_path, "wb") as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )


def pre_renderer(configurator):
    """Pre rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "upgrade_step"
    upgrade_step_source_version = _read_source_version(configurator)
    upgrade_step_dest_version = upgrade_step_source_version + 1
    configurator.variables["upgrade_step_source_version"] = upgrade_step_source_version
    configurator.variables["upgrade_step_dest_version"] = upgrade_step_dest_version
    configurator.variables["upgrade_step_id"] = str(upgrade_step_dest_version)
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_package_configure_zcml(configurator)
    _update_upgrades_configure_zcml(configurator)
    _write_dest_version(configurator)
    _remove_unwanted_files(configurator)
    git_commit(
        configurator,
        "Add upgrade_step: {0}".format(
            configurator.variables["upgrade_step_title"],
        ),
    )
