# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import update_file
from lxml import etree

import os
import stringcase


def _update_package_configure_zcml(configurator):
    file_name = u'configure.zcml'
    file_path = configurator.variables['package_folder'] + '/' + file_name
    nsprefix = '{http://namespaces.zope.org/zope}'

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = '.vocabularies'
        xpath_selector = ".//{0}include[@package='{1}']".format(
            nsprefix,
            permid,
        )  # NOQA: S100
        if len(tree_root.findall(xpath_selector)):
            print('{0} already in configure.zcml, skip adding!'.format(permid))
            return

    match_str = '-*- extra stuff goes here -*-'
    insert_str = """
    <include package=".vocabularies" />

        """
    update_file(configurator, file_path, match_str, insert_str)


def _update_vocabularies_configure_zcml(configurator):
    file_name = u'configure.zcml'
    file_path = configurator.variables[
        'package_folder'] + '/vocabularies/' + file_name
    example_file_path = file_path + '.example'
    file_list = os.listdir(os.path.dirname(file_path))
    if file_name not in file_list:
        os.rename(example_file_path, file_path)

    nsprefix = '{http://namespaces.zope.org/zope}'

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        vocab_name = '{0}.{1}'.format(
            configurator.variables['package.dottedname'],
            configurator.variables['vocabulary_name_klass'],
        )
        xpath_selector = ".//{0}utility[@name='{1}']".format(
            nsprefix,
            vocab_name,
        )
        if len(tree_root.findall(xpath_selector)):
            print('{0} already in configure.zcml, skip adding!'.format(vocab_name))  # NOQA: E501
            return

    match_str = '-*- extra stuff goes here -*-'
    insert_str = """
    <utility
        component=".{0}.{1}Factory"
        name="{2}.{1}"
    />

        """.format(
        configurator.variables['vocabulary_name_normalized'],
        configurator.variables['vocabulary_name_klass'],
        configurator.variables['package.dottedname'],
    )
    update_file(configurator, file_path, match_str, insert_str)


def prepare_renderer(configurator):
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = 'vocabulary'
    vocabulary_name = configurator.variables['vocabulary_name'].strip('_')
    configurator.variables['vocabulary_name_klass'] = stringcase.pascalcase(
        vocabulary_name)
    configurator.variables['vocabulary_name_normalized'] = stringcase.snakecase(  # NOQA: E501
        vocabulary_name)
    configurator.target_directory = configurator.variables['package_folder']


def post_renderer(configurator):
    """"""
    _update_package_configure_zcml(configurator)
    _update_vocabularies_configure_zcml(configurator)
