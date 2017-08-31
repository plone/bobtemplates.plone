# -*- coding: utf-8 -*-

from mrbob.bobexceptions import ValidationError
from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import logger
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import is_string_in_file
from lxml import etree
import re


def post_theme_name(configurator, question, answer):
    regex = r'^\w+[a-zA-Z0-9 \.\-_]*\w$'
    if not re.match(regex, answer):
        msg = u"Error: '{0}' is not a valid themename.\n".format(answer)
        msg += u"Please use a valid name (like 'Tango' or 'my-tango.com')!\n"
        msg += u"At beginning or end only letters|diggits are allowed.\n"
        msg += u"Inside the name also '.-_' are allowed.\n"
        msg += u"No umlauts!"
        raise ValidationError(msg)
    return answer


def prepare_renderer(configurator):
    logger.info("Using plone_theme template:")
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = 'theme'

    def normalize_theme_name(value):
        value = "-".join(value.split('_'))
        value = "-".join(value.split())
        return value
    configurator.variables[
        "theme.normalized_name"] = normalize_theme_name(
            configurator.variables.get('theme.name')).lower()


def _update_configure_zcml(configurator):
    file_name = u'configure.zcml'
    file_path = configurator.variables['package_folder'] + '/' + file_name
    namespaces = {'plone': 'http://namespaces.plone.org/plone'}

    with open(file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        tree_root = tree.getroot()
        theme_name = configurator.variables['theme.normalized_name']
        theme_xpath = "./plone:static[@name='{0}']".format(theme_name)
        if len(tree_root.xpath(theme_xpath, namespaces=namespaces)):
            print("%s already in configure.zcml, skip adding!" % theme_name)
            return

    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <plone:static
      directory="theme"
      type="theme"
      name="{0}"
      />

        """.format(configurator.variables['theme.normalized_name'])
    update_file(configurator, file_path, match_str, insert_str)


def _update_setup_py(configurator):
    file_name = u'setup.py'
    file_path = configurator.variables['package.root_folder'] + '/' + file_name
    match_str = "-*- Extra requirements: -*-"
    insert_strings = [
        'collective.themesitesetup',
        'collective.themefragments',
    ]
    for insert_str in insert_strings:
        insert_str = "        '{0}',\n".format(insert_str)
        if is_string_in_file(configurator, file_path, insert_str):
            continue
        update_file(configurator, file_path, match_str, insert_str)


def post_renderer(configurator):
    """
    """
    _update_configure_zcml(configurator)
    _update_setup_py(configurator)
