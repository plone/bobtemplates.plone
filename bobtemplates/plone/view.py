from bobtemplates.plone.base import prepare_renderer_for_subtemplate
from bobtemplates.plone.base import get_klass_name
from bobtemplates.plone.base import get_normalized_name
from bobtemplates.plone.base import create_file_if_not_exists
from bobtemplates.plone.base import update_file
from bobtemplates.plone.base import get_file_path
from bobtemplates.plone.base import get_example_file_path
from bobtemplates.plone.base import write_xml_tree_to_file
from bobtemplates.plone.base import get_xml_tree
from bobtemplates.plone.base import add_xml_tag_to_root
from bobtemplates.plone.base import get_browser_namespace
from lxml import etree

import os

def _update_views_py(configurator):
    views_file_name = u'views.py'
    views_dir = u'browser'

    views_file_path = get_file_path(configurator, views_dir, views_file_name)
    views_example_file_path = get_example_file_path(configurator, views_dir, views_file_name)
    create_file_if_not_exists(views_file_path, views_example_file_path)

    match_str = '-*- Extra views go here -*-'
    insert_str = """
class {0}View(BrowserView):
    \"\"\" {1} \"\"\"
    
    def the_title():
        return u'{2}'
    """
    insert_str = insert_str.format(
        configurator.variables['view_name_klass'],
        configurator.variables['description'],
        configurator.variables['title']
    )
    
    update_file(configurator, views_file_path, insert_str, match_str)
    return


def _update_configure_zcml(configurator):
    file_name = u'configure.zcml'
    dir_name = u'browser'
    file_path = get_file_path(configurator, dir_name, file_name) 

    attributes = {
        'name': configurator.variables['view_name_normalized'] ,
        'for': '*',
        'class': \
            '.views.' + configurator.variables['view_name_klass'] + 'View',
        'template': 'templates/' + \
            configurator.variables['view_name_normalized'] + '.pt',
        'permission': 'zope2.View'
    }

    tag = get_browser_namespace() + 'page'
    add_xml_tag_to_root(file_path, tag, attributes)
    return


def prepare_renderer(configurator):
    configurator = prepare_renderer_for_subtemplate(configurator,
                                                    subtemplate='view')
    view_name = configurator.variables['view_name']
    configurator.variables['view_name_klass'] = get_klass_name(view_name) 
    configurator.variables['view_name_normalized'] = \
        get_normalized_name(view_name)

def post_renderer(configurator):
    _update_views_py(configurator)
    _update_configure_zcml(configurator)
