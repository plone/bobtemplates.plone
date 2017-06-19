from mrbob.bobexceptions import ValidationError
from lxml import etree
import keyword
import logging
import re
import os

log = logging.getLogger("bobtemplates.plone")


def _get_package_root_folder():
    file_name = 'setup.py'
    cur_dir = os.getcwd()
    while True:
        files = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in files:
            break
        else:
            if cur_dir == parent_dir:
                break
            cur_dir = parent_dir
    return cur_dir


def check_dexterity_type_name(configurator, question, answer):
    if keyword.iskeyword(answer):
        raise ValidationError('%s is a reserved Python keyword' % answer)
    if not re.match('[_a-zA-Z ]*$', answer):
        raise ValidationError('%s is not a valid identifier' % answer)
    return answer


def prepare_render(configurator):
    """ Some variables to make templating easier.
    """
    # TODO: find out package.dottedname from parent package:
    root_folder = _get_package_root_folder()
    configurator.variables['package.dottedname'] = root_folder.split('/')[-1]
    type_name = configurator.variables['dexterity_type_name']
    configurator.variables[
        'dexterity_type_name_klass'] = type_name.title().replace(' ', '')
    configurator.variables[
        'dexterity_type_name_normalized'] = type_name.replace(' ', '_').lower()


def _update_types_xml(configurator):
    """ Add the new type to types.xml in Generic Setup profiles.
    """
    types_file_name = u'types.xml'
    types_file_dir = u'profiles/default'
    types_file_path = types_file_dir + '/' + types_file_name
    file_list = os.listdir(
        os.path.dirname(types_file_path))
    if types_file_name not in file_list:
        os.rename(types_file_dir + '/types.xml.example', types_file_path)

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


def post_renderer(configurator):
    """
    """
    _update_types_xml(configurator)

    print("""vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

Now add the follwing to profiles/default/types.xml:

    <object name="%s" meta_type="Dexterity FTI"/>
    """ % configurator.variables['dexterity_type_name_normalized'])
