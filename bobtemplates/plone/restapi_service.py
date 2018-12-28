# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import is_string_in_file
from bobtemplates.plone.base import remove_unwanted_files
from bobtemplates.plone.base import update_configure_zcml
from bobtemplates.plone.base import update_file

import case_conversion as cc


# from mrbob.bobexceptions import SkipQuestion
# from mrbob.bobexceptions import ValidationError


def get_service_name_from_python_class(configurator, question):
    """Get default service_name from python class"""
    class_name = configurator.variables['service_class_name']
    if class_name:
        generated_name = cc.snakecase(class_name).replace('_', '-')
        question.default = generated_name
    else:
        question.default = 'my-service'


def _update_package_configure_zcml(configurator):
    path = '{0}'.format(
        configurator.variables['package_folder'],
    )
    file_name = u'configure.zcml'
    match_xpath = "include[@package='.api']"
    match_str = '-*- extra stuff goes here -*-'
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
    path = '{0}/api'.format(
        configurator.variables['package_folder'],
    )
    file_name = u'configure.zcml'
    example_file_name = '{0}.example'.format(file_name)
    match_xpath = "include[@package='.services']"
    match_str = '-*- extra stuff goes here -*-'
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
    path = '{0}/api/services'.format(
        configurator.variables['package_folder'],
    )
    file_name = u'configure.zcml'
    example_file_name = '{0}.example'.format(file_name)
    match_xpath = "include[@package='.{0}']".format(
        configurator.variables['service_class_name_normalized'],
    )
    match_str = '-*- extra stuff goes here -*-'
    insert_str = '<include package=".{0}" />\n'.format(
        configurator.variables['service_class_name_normalized'],
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


def _update_setup_py(configurator):
    file_name = u'setup.py'
    file_path = configurator.variables['package.root_folder'] + '/' + file_name
    match_str = '-*- Extra requirements: -*-'
    insert_strings = [
        'plone.restapi',
    ]
    for insert_str in insert_strings:
        insert_str = "        '{0}',\n".format(insert_str)
        if is_string_in_file(configurator, file_path, insert_str):
            continue
        update_file(configurator, file_path, match_str, insert_str)


def _remove_unwanted_files(configurator):
    file_paths = []
    rel_file_paths = [
        '/api/configure.zcml.example',
        '/api/services/configure.zcml.example',
    ]
    base_path = configurator.variables['package_folder']
    for rel_file_path in rel_file_paths:
        file_paths.append('{0}{1}'.format(base_path, rel_file_path))
    remove_unwanted_files(file_paths)


def pre_renderer(configurator):
    """Pre rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = 'restapi_service'
    name = configurator.variables['service_name'].strip('_')
    name_normalized = cc.snakecase(name)
    configurator.variables['service_name_normalized'] = name_normalized
    class_name = configurator.variables['service_class_name'].strip('_')  # NOQA: E501
    configurator.variables['service_class_name'] = cc.pascalcase(     # NOQA: E501
        class_name,
    )
    configurator.variables['service_class_name_normalized'] = cc.snakecase(
        class_name,
    )
    configurator.target_directory = configurator.variables['package_folder']


def post_renderer(configurator):
    """Post rendering."""
    _update_package_configure_zcml(configurator)
    _update_api_configure_zcml(configurator)
    _update_services_configure_zcml(configurator)
    # _remove_unwanted_files(configurator)
    git_commit(
        configurator,
        'Add restapi_service: {0}'.format(
            configurator.variables['service_name'],
        ),
    )
