# -*- coding: utf-8 -*-
from datetime import date
from lxml import etree
from mrbob.bobexceptions import MrBobError
from mrbob.bobexceptions import ValidationError

import logging
import os
import sys


try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


logger = logging.getLogger('bobtemplates.plone')


class SetupCfg(object):
    def __init__(self):
        self.version = None


def read_setup_cfg(configurator):
    setup_cfg = SetupCfg()
    config = ConfigParser()
    path = configurator.target_directory + '/setup.cfg'
    config.read(path)
    if not config.sections():
        return
    setup_cfg.version = config.get('tool:bobtemplates.plone', 'version')
    return setup_cfg


def set_global_vars(configurator):
    setup_cfg = read_setup_cfg(configurator)
    configurator.variables['year'] = date.today().year
    version = configurator.variables.get('plone.version')
    if not version and setup_cfg:
        print('>>> reading Plone version from setup.cfg...')
        version = setup_cfg.version
    _set_plone_version_variables(configurator, version)


def _set_plone_version_variables(configurator, version):
    version = configurator.variables.get('plone.version', version)
    if not version:
        return
    if 'plone.is_plone5' not in configurator.variables:
        # Find out if it is supposed to be Plone 5.
        if version.startswith('5'):
            configurator.variables['plone.is_plone5'] = True
        else:
            configurator.variables['plone.is_plone5'] = False
    if 'plone.minor_version' not in configurator.variables:
        # extract minor version (4.3)
        # (according to https://plone.org/support/version-support-policy)
        # this is used for the trove classifier in setup.py of the product
        configurator.variables['plone.minor_version'] = \
            '.'.join(version.split('.')[:2])


def is_string_in_file(configurator, file_path, match_str):
    """Simple check if a given string is in a file.

    You can use this before adding new lines with update_file.

    """
    with open(file_path, 'r+') as xml_file:
        contents = xml_file.readlines()
    for index, line in enumerate(contents):
        if match_str in line:
            return True
    return False


def write_xml_tree_to_file(tree, file_path):
    with open(file_path, 'wb') as xml_file:
        tree.write(
            xml_file,
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8',
        )
    return


def update_file(configurator, file_path, match_str, insert_str):
    """Insert insert_str into given file, by match_str."""
    changed = False

    with open(file_path, 'r+') as xml_file:
        contents = xml_file.readlines()
        if match_str in contents[-1]:  # Handle last line, prev. IndexError
            contents.append(insert_str)
            changed = True
        else:
            for index, line in enumerate(contents):
                if (
                    match_str in line and
                    insert_str not in contents[index + 1]
                ):
                    contents.insert(index + 1, insert_str)
                    changed = True
                    break
        xml_file.seek(0)
        xml_file.writelines(contents)

    if not changed:
        print(
            "WARNING: We couldn't find the match_str, "  # NOQA
            "skip inserting into {0}:\n".format(file_path)  # NOQA
        )
        print(insert_str)


def get_xml_tree(xml_file):
    parser = etree.getXMLParser(remove_blank_text=True)
    tree = etree.parse(xml_file, parser)
    return tree


def add_xml_tag_to_root(file_path, tag, attributes):
    with open(file_path, 'r') as xml_file:
        tree = get_xml_tree(xml_file)
        configure_tag = tree.getroot()

        etree.SubElement(configure_tag, tag, attrib=attributes)

    write_xml_tree_to_file(tree, file_path)
    return


def create_file_if_not_exists(file_path, example_file_path):
    file_list = os.listdir(os.path.dirname(file_path))
    file_name = os.path.basename(file_path)
    if file_name not in file_list:
        os.rename(example_file_path, file_path)
    return


def _get_package_root_folder(configurator):
    file_name = 'setup.py'
    root_folder = None
    os.chdir(configurator.target_directory)
    cur_dir = os.getcwd()
    while True:
        files = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in files:
            root_folder = cur_dir
            break
        else:
            if cur_dir == parent_dir:
                break
            cur_dir = parent_dir
    return root_folder


def get_file_path(configurator, dir_name, file_name):
    file_path = os.path.join(
        os.path.join(configurator.target_directory, dir_name),
        file_name,
    )
    return file_path


def get_example_file_path(configurator, dir_name, file_name):
    example_file_name = file_name + '.example'
    example_file_path = get_file_path(
        configurator, dir_name, example_file_name,
    )
    return example_file_path


def check_root_folder(configurator, question):
    """Check if we are in a package.

    Should be called in first question pre hook.

    """
    root_folder = _get_package_root_folder(configurator)
    if not root_folder:
        raise ValidationError(
            '\n\nNo setup.py found in path!\n'
            'Please run this subtemplate inside an existing package,\n'
            'in the package dir, where the actual code is!\n'
            "In the package collective.dx it's in collective.dx/collective/dx"
            '\n')


def dottedname_to_path(dottedname):
    path = '/'.join(dottedname.split('.'))
    return path


def get_klass_name(name):
    klass_name = name.title().replace(' ', '')
    return klass_name


def get_normalized_name(name):
    normalized_name = name.replace(' ', '_').lower()
    return normalized_name


def base_prepare_renderer(configurator):
    """generic rendering before template specific rendering."""
    configurator.variables['package.root_folder'] = _get_package_root_folder(
        configurator,
    )
    if not configurator.variables['package.root_folder']:
        raise MrBobError('No setup.py found in path!\n')
    configurator.variables['package.dottedname'] = \
        configurator.variables['package.root_folder'].split('/')[-1]
    configurator.variables['package.namespace'] = \
        configurator.variables['package.dottedname'].split('.')[0]
    configurator.variables['package.name'] = \
        configurator.variables['package.dottedname'].split('.')[-1]
    # package.uppercasename = 'COLLECTIVE_FOO_SOMETHING'
    configurator.variables['package.uppercasename'] = \
        configurator.variables['package.dottedname'].replace('.', '_').upper()

    package_subpath = dottedname_to_path(
        configurator.variables['package.dottedname'],
    )
    configurator.variables['package_folder'] = \
        configurator.variables['package.root_folder'] + \
        u'/src/' + package_subpath
    configurator.target_directory = \
        configurator.variables['package.root_folder']
    return configurator


def subtemplate_warning(configurator, question):
    """Show a warning to the user before using subtemplates!"""
    print("""
    ### WARNING ###

    This is a subtemplate, it might override existing files without warnings!
    Please use a version control system like GIT with a clean state,
    to track changes, before using this subtemplate!

    """)


def subtemplate_warning_post_question(configurator, question, answer):
    if answer.lower() != 'yes':
        print('Abort!')
        sys.exit(0)
    return answer


def prepare_renderer_for_subtemplate(configurator, subtemplate):
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = subtemplate
    configurator.target_directory = configurator.variables['package_folder']
    return configurator
