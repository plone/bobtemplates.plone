# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import is_string_in_file
from bobtemplates.plone.base import update_file
from lxml import etree
from mrbob.bobexceptions import ValidationError

import keyword
import os
import re


def check_dexterity_type_name(configurator, question, answer):
    if keyword.iskeyword(answer):
        raise ValidationError(u'{key} is a reserved Python keyword'.format(key=answer))  # NOQA: E501
    if not re.match('[_a-zA-Z ]*$', answer):
        raise ValidationError(u'{key} is not a valid identifier'.format(key=answer))  # NOQA: E501
    return answer


def _update_metadata_xml(configurator):
    """Add plone.app.dexterity dependency metadata.xml in Generic Setup
    profiles."""
    metadata_file_name = u'metadata.xml'
    metadata_file_dir = u'profiles/default'
    metadata_file_path = configurator.variables['package_folder'] + '/' + \
        metadata_file_dir + '/' + metadata_file_name

    with open(metadata_file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        dependencies = tree.xpath('/metadata/dependencies')[0]
        deps = [
            'profile-plone.app.dexterity:default',
        ]
        if not configurator.variables['plone.is_plone5']:
            deps.append('profile-plone.app.relationfield:default')
        changed = False
        for dep in deps:
            dep_exists = False
            for e in dependencies.iter('dependency'):
                dep_name = e.text
                if dep_name in dep:
                    dep_exists = True
            if dep_exists:
                print(
                    '{dep} already in metadata.xml, skip adding!'.format(
                        dep=dep,
                    ),
                )
                continue
            dep_element = etree.Element('dependency')
            dep_element.text = dep
            dependencies.append(dep_element)
            changed = True

    if not changed:
        return

    with open(metadata_file_path, 'wb') as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8',
        )


def _update_types_xml(configurator):
    """Add the new type to types.xml in Generic Setup profiles."""
    types_file_name = u'types.xml'
    types_file_dir = u'profiles/default'
    types_file_path = configurator.target_directory + '/' + types_file_dir +\
        '/' + types_file_name
    types_example_file_path = configurator.target_directory + '/' +\
        types_file_dir + '/types.xml.example'
    file_list = os.listdir(os.path.dirname(types_file_path))
    if types_file_name not in file_list:
        os.rename(types_example_file_path, types_file_path)

    with open(types_file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        types = tree.xpath("/object[@name='portal_types']")[0]
        type_name = configurator.variables['dexterity_type_name_normalized']
        if len(types.xpath("./object[@name='{name}']".format(name=type_name))):
            print('{name} already in types.xml, skip adding!'.format(name=type_name))  # NOQA: E501
            return
        types.append(
            etree.Element('object', name=type_name, meta_type='Dexterity FTI'),
        )

    with open(types_file_path, 'wb') as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8',
        )


def _update_rolemap_xml(configurator):
    file_name = u'rolemap.xml'
    file_path = '{0}/profiles/default/{1}'.format(
        configurator.variables['package_folder'],
        file_name,
    )

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permname = '{0}: Add {1}'.format(
            configurator.variables['package.dottedname'],
            configurator.variables['dexterity_type_name_klass'],
        )
        xpath_selector = ".//permission[@name='{0}']".format(permname)
        if len(tree_root.findall(xpath_selector)):
            print('{name} already in rolemap.xml, skip adding!'.format(name=permname))  # NOQA: E501
            return

    match_str = '-*- extra stuff goes here -*-'
    insert_str = """
    <permission name="{0}: Add {1}" acquire="True">
      <role name="Manager"/>
      <role name="Site Administrator"/>
      <role name="Owner"/>
      <role name="Contributor"/>
    </permission>

        """.format(
        configurator.variables['package.dottedname'],
        configurator.variables['dexterity_type_name_klass'],
    )
    update_file(configurator, file_path, match_str, insert_str)


def _update_permissions_zcml(configurator):
    file_name = u'permissions.zcml'
    file_path = configurator.variables['package_folder'] + '/' + file_name
    nsprefix = '{http://namespaces.zope.org/zope}'

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = '{0}.Add{1}'.format(
            configurator.variables['package.dottedname'],
            configurator.variables['dexterity_type_name_klass'],
        )
        xpath_selector = ".//{0}permission[@id='{1}']".format(nsprefix, permid)
        if len(tree_root.findall(xpath_selector)):
            print('{permission} already in permissions.zcml, skip adding!'.format(permission=permid))  # NOQA: E501
            return

    match_str = '-*- extra stuff goes here -*-'
    insert_str = """
    <permission
        id="{0}.Add{1}"
        title="{0}: Add {1}"
    />

        """.format(
        configurator.variables['package.dottedname'],
        configurator.variables['dexterity_type_name_klass'],
    )
    update_file(configurator, file_path, match_str, insert_str)


def _update_setup_py(configurator):
    file_name = u'setup.py'
    file_path = configurator.variables['package.root_folder'] + '/' + file_name
    match_str = '-*- Extra requirements: -*-'
    insert_strings = [
        'plone.app.dexterity',
    ]
    for insert_str in insert_strings:
        insert_str = "        '{0}',\n".format(insert_str)
        if is_string_in_file(configurator, file_path, insert_str):
            continue
        update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = 'content_type'
    type_name = configurator.variables['dexterity_type_name']
    configurator.variables['dexterity_type_name_klass'] = type_name.title().replace(' ', '')  # NOQA: E501
    configurator.variables['dexterity_type_name_normalized'] = type_name.replace(' ', '_').lower()  # NOQA: E501
    configurator.target_directory = configurator.variables['package_folder']


def post_renderer(configurator):
    """"""
    _update_types_xml(configurator)
    _update_permissions_zcml(configurator)
    _update_rolemap_xml(configurator)
    _update_metadata_xml(configurator)
    _update_setup_py(configurator)
