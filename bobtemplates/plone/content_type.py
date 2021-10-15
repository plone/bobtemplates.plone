# -*- coding: utf-8 -*-
"""Generate content type."""

import keyword
import os
import re

from lxml import etree
from mrbob.bobexceptions import SkipQuestion, ValidationError

from bobtemplates.plone.base import (
    base_prepare_renderer,
    get_normalized_classname,
    get_normalized_dxtypename,
    get_normalized_ftiname,
    git_commit,
    update_file,
)
from bobtemplates.plone.utils import run_black, run_isort


def is_container(configurator, question):
    """Test if base class is a container."""
    if configurator.variables["dexterity_type_base_class"] != "Container":
        raise SkipQuestion(u"Is not a Container, so we skip filter question.")


def supermodel_is_used(configurator, question):
    """Test if supermodel is used."""
    if configurator.variables.get("dexterity_type_supermodel", False):
        raise SkipQuestion(
            u"Skip question, because we need a base class ",
            u"when supermodel ist used.",
        )


def check_dexterity_type_name(configurator, question, answer):
    """Test if type name is valid."""
    if keyword.iskeyword(answer):
        raise ValidationError(
            u'"{key}" is a reserved Python keyword!'.format(key=answer)
        )  # NOQA: E501
    if not re.match("[_a-zA-Z ]*$", answer):
        raise ValidationError(
            u'"{key}" is not a valid identifier!\n'
            u"Allowed characters: _ a-z A-Z and whitespace.\n".format(
                key=answer
            ),  # NOQA: E501
        )
    return answer


def check_global_allow(configurator, answer):
    """Skip parent container name if global_allow is true."""
    if configurator.variables.get("dexterity_type_global_allow", False):
        raise SkipQuestion(
            u"global_allow is true, so we skip parent container name question."
        )  # NOQA: E501


def _update_metadata_xml(configurator):
    """Add plone.app.dexterity dependency metadata.xml in Generic Setup profiles."""  # NOQA: E501
    metadata_file_name = u"metadata.xml"
    metadata_file_dir = u"profiles/default"
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
        deps = [
            "profile-plone.app.dexterity:default",
        ]
        changed = False
        for dep in deps:
            dep_exists = False
            for e in dependencies.iter("dependency"):
                dep_name = e.text
                if dep_name in dep:
                    dep_exists = True
            if dep_exists:
                print(
                    "{dep} already in metadata.xml, skip adding!".format(
                        dep=dep,
                    ),
                )
                continue
            dep_element = etree.Element("dependency")
            dep_element.text = dep
            dependencies.append(dep_element)
            changed = True

    if not changed:
        return

    with open(metadata_file_path, "wb") as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )


def _update_types_xml(configurator):
    """Add the new type to types.xml in Generic Setup profiles."""
    types_file_name = u"types.xml"
    types_file_dir = u"profiles/default"
    types_file_path = (
        configurator.target_directory + "/" + types_file_dir + "/" + types_file_name
    )
    types_example_file_path = (
        configurator.target_directory + "/" + types_file_dir + "/types.xml.example"
    )
    file_list = os.listdir(os.path.dirname(types_file_path))
    if types_file_name not in file_list:
        os.rename(types_example_file_path, types_file_path)

    with open(types_file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        types = tree.xpath("/object[@name='portal_types']")[0]
        type_name = configurator.variables["dexterity_type_name"]
        if len(types.xpath("./object[@name='{name}']".format(name=type_name))):
            print(
                "{name} already in types.xml, skip adding!".format(name=type_name)
            )  # NOQA: E501
            return
        types.append(
            etree.Element("object", name=type_name, meta_type="Dexterity FTI"),
        )

    with open(types_file_path, "wb") as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )


def _update_parent_types_fti_xml(configurator):
    parent_ct_name = configurator.variables.get(
        "dexterity_parent_container_type_name"
    )  # NOQA: E501
    if not parent_ct_name:
        return
    parent_dexterity_type_fti_file_name = get_normalized_ftiname(
        parent_ct_name
    )  # NOQA: E501
    file_name = u"{0}.xml".format(
        parent_dexterity_type_fti_file_name,
    )
    file_path = "{0}/profiles/default/types/{1}".format(
        configurator.variables["package_folder"],
        file_name,
    )

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        type_name = configurator.variables["dexterity_type_name"]
        if len(
            tree.xpath(".//element[@value='{name}']".format(name=type_name))
        ):  # NOQA: E501
            print(
                "{name} already in {filename}, skip adding!".format(
                    name=type_name,
                    filename=file_name,
                ),
            )
            return

    match_str = """<property name="allowed_content_types">"""
    insert_str = """    <element value="{0}" />
    """.format(
        configurator.variables["dexterity_type_name"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def _update_rolemap_xml(configurator):
    file_name = u"rolemap.xml"
    file_path = "{0}/profiles/default/{1}".format(
        configurator.variables["package_folder"],
        file_name,
    )

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permname = "{0}: Add {1}".format(
            configurator.variables["package.dottedname"],
            configurator.variables["dexterity_type_name_klass"],
        )
        xpath_selector = ".//permission[@name='{0}']".format(permname)
        if len(tree_root.findall(xpath_selector)):
            print(
                "{name} already in rolemap.xml, skip adding!".format(name=permname)
            )  # NOQA: E501
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <permission name="{0}: Add {1}" acquire="True">
      <role name="Manager"/>
      <role name="Site Administrator"/>
      <role name="Owner"/>
      <role name="Contributor"/>
    </permission>

""".format(
        configurator.variables["package.dottedname"],
        configurator.variables["dexterity_type_name_klass"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def _update_permissions_zcml(configurator):
    file_name = u"permissions.zcml"
    file_path = configurator.variables["package_folder"] + "/" + file_name
    nsprefix = "{http://namespaces.zope.org/zope}"

    with open(file_path, "r") as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = "{0}.Add{1}".format(
            configurator.variables["package.dottedname"],
            configurator.variables["dexterity_type_name_klass"],
        )
        xpath_selector = ".//{0}permission[@id='{1}']".format(nsprefix, permid)
        if len(tree_root.findall(xpath_selector)):
            print(
                "{permission} already in permissions.zcml, skip adding!".format(
                    permission=permid
                )
            )  # NOQA: E501
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
    <permission
        id="{0}.Add{1}"
        title="{0}: Add {1}"
    />

""".format(
        configurator.variables["package.dottedname"],
        configurator.variables["dexterity_type_name_klass"],
    )
    update_file(configurator, file_path, match_str, insert_str)


def pre_ask(configurator):
    """Empty pre ask."""


def prepare_renderer(configurator):
    """Prepare rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "content_type"
    type_name = configurator.variables["dexterity_type_name"]
    dx_type_name_klass = get_normalized_classname(type_name)
    configurator.variables["dexterity_type_name_klass"] = dx_type_name_klass
    dx_type_fti_file_name = get_normalized_ftiname(type_name)
    configurator.variables[
        "dexterity_type_fti_file_name"
    ] = dx_type_fti_file_name  # NOQA: E501
    dx_type_name_normalized = get_normalized_dxtypename(type_name)
    configurator.variables[
        "dexterity_type_name_normalized"
    ] = dx_type_name_normalized  # NOQA: E501
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_types_xml(configurator)
    _update_parent_types_fti_xml(configurator)
    _update_permissions_zcml(configurator)
    _update_rolemap_xml(configurator)
    _update_metadata_xml(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add content_type: {0}".format(
            configurator.variables["dexterity_type_name"],
        ),
    )
