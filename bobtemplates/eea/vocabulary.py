# -*- coding: utf-8 -*-

from bobtemplates.eea.base import base_prepare_renderer
from bobtemplates.eea.base import echo
from bobtemplates.eea.base import git_commit
from bobtemplates.eea.base import update_file
from bobtemplates.eea.base import ZCML_NAMESPACES
from lxml import etree

import case_conversion as cc
import os


def _update_package_configure_zcml(configurator):
    file_name = u'configure.zcml'
    file_path = configurator.variables['package_folder'] + '/' + file_name

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        permid = '.vocabularies'
        xpath_selector = "./include[@package='{0}']".format(permid)  # NOQA: E501
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
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

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        vocab_name = '{0}.{1}'.format(
            configurator.variables['package.dottedname'],
            configurator.variables['vocabulary_name_klass'],
        )
        xpath_selector = "./utility[@name='{0}']".format(
            vocab_name,
        )
        if len(tree_root.xpath(xpath_selector, namespaces=ZCML_NAMESPACES)):
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
    configurator.variables['vocabulary_name_klass'] = cc.pascalcase(
        vocabulary_name)
    configurator.variables['vocabulary_name_normalized'] = cc.snakecase(  # NOQA: E501
        vocabulary_name)
    configurator.target_directory = configurator.variables['package_folder']


def post_renderer(configurator):
    """"""
    _update_package_configure_zcml(configurator)
    _update_vocabularies_configure_zcml(configurator)
    git_commit(
        configurator,
        'Add vocabulary: {0}'.format(
            configurator.variables['vocabulary_name'],
        ),
    )
    registered_vocabulary = '{0}.{1}'.format(
        configurator.variables['package.dottedname'],
        configurator.variables['vocabulary_name_klass'],
    )
    echo(
        '------------------------\nSucessfully added: {0} template.\n'.format(
            configurator.variables['template_id'],
        ),
    )
    echo(
        'You can lookup your vocabulary by the name: {0}\n'.format(
            registered_vocabulary,
        ),
        'info',
    )
