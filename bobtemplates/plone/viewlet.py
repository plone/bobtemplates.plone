# -*- coding: utf-8 -*-
from bobtemplates.plone.base import add_xml_tag_to_root
from bobtemplates.plone.base import create_file_if_not_exists
from bobtemplates.plone.base import get_browser_namespace
from bobtemplates.plone.base import get_example_file_path
from bobtemplates.plone.base import get_file_path
from bobtemplates.plone.base import get_klass_name
from bobtemplates.plone.base import get_normalized_name
from bobtemplates.plone.base import prepare_renderer_for_subtemplate
from bobtemplates.plone.base import update_file

from collections import OrderedDict


def _update_viewlets_py(configurator):
    file_name = u'viewlets.py'
    dir_name = u'browser'

    file_path = get_file_path(configurator, dir_name, file_name)
    example_file_path = get_example_file_path(
        configurator, dir_name, file_name,
    )
    create_file_if_not_exists(file_path, example_file_path)

    match_str = '-*- Extra viewlets go here -*-'
    insert_str = """
class {0}Viewlet(ViewletBase):
    \"\"\" {1} \"\"\"
    pass
    """

    insert_str = insert_str.format(
        configurator.variables['viewlet_name_klass'],
        configurator.variables['title'],
    )

    update_file(configurator, file_path, insert_str, match_str)
    return


def _update_configure_zcml(configurator):
    file_name = u'configure.zcml'
    dir_name = u'browser'
    file_path = get_file_path(configurator, dir_name, file_name)

    attributes = OrderedDict([
        ('name', configurator.variables['viewlet_name_normalized']),
        ('for', '*'),
        ('manager', 'plone.app.layout.viewlets.interfaces.I' +
         configurator.variables['manager_name_klass']),
        ('class', '.viewlets.' + configurator.variables['viewlet_name_klass'] +
         'Viewlet'),
        ('layer', 'zope.interface.Interface'),
        ('template', 'templates/' +
         configurator.variables['viewlet_name_normalized'] + '.pt'),
        ('permission', 'zope2.View'),
    ])

    tag = get_browser_namespace() + 'viewlet'
    add_xml_tag_to_root(file_path, tag, attributes)
    return


def prepare_renderer(configurator):
    configurator = prepare_renderer_for_subtemplate(
        configurator, subtemplate='viewlet',
    )
    name = configurator.variables['viewlet_name']
    configurator.variables['viewlet_name_klass'] = get_klass_name(name)
    configurator.variables['viewlet_name_normalized'] = \
        get_normalized_name(name)
    configurator.variables['manager_name_klass'] = \
        get_klass_name(configurator.variables['manager'])
    return


def post_renderer(configurator):
    _update_configure_zcml(configurator)
    _update_viewlets_py(configurator)
    return
