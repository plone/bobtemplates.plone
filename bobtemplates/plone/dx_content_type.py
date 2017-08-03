from bobtemplates.plone.subcommand import base_prepare_renderer
from bobtemplates.plone.subcommand import dottedname_to_path
from bobtemplates.plone.subcommand import logger
from mrbob.bobexceptions import ValidationError
from lxml import etree
import keyword
import re
import os


def check_dexterity_type_name(configurator, question, answer):
    if keyword.iskeyword(answer):
        raise ValidationError('%s is a reserved Python keyword' % answer)
    if not re.match('[_a-zA-Z ]*$', answer):
        raise ValidationError('%s is not a valid identifier' % answer)
    return answer


def _update_types_xml(configurator):
    """ Add the new type to types.xml in Generic Setup profiles.
    """
    types_file_name = u'types.xml'
    types_file_dir = u'profiles/default'
    types_file_path = configurator.target_directory + '/' + types_file_dir +\
        '/' + types_file_name
    types_example_file_path = configurator.target_directory + '/' +\
        types_file_dir + '/types.xml.example'
    file_list = os.listdir(
        os.path.dirname(types_file_path))
    if types_file_name not in file_list:
        os.rename(types_example_file_path, types_file_path)

    with open(types_file_path, 'r') as xml_file:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        types = tree.xpath("/object[@name='portal_types']")[0]
        type_name = configurator.variables['dexterity_type_name_normalized']
        if len(types.xpath("./object[@name='%s']" % type_name)):
            print("%s already in types.xml, skip adding!" % type_name)
            return
        types.append(
            etree.Element('object', name=type_name, meta_type='Dexterity FTI'))

    with open(types_file_path, 'w') as xml_file:
        tree.write(
            xml_file, pretty_print=True, xml_declaration=True,
            encoding="utf-8")


def prepare_renderer(configurator):
    logger.info("Using dx_content_type template:")
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = 'dx_content_type'
    type_name = configurator.variables['dexterity_type_name']
    configurator.variables[
        'dexterity_type_name_klass'] = type_name.title().replace(' ', '')
    configurator.variables[
        'dexterity_type_name_normalized'] = type_name.replace(' ', '_').lower()
    package_subpath = dottedname_to_path(
        configurator.variables['package.dottedname'])
    configurator.target_directory += u'/src/' + package_subpath


def post_renderer(configurator):
    """
    """
    _update_types_xml(configurator)
