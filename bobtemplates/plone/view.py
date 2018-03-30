# -*- coding: utf-8 -*-
from bobtemplates.plone.base import create_file_if_not_exists
from bobtemplates.plone.base import get_browser_namespace
from bobtemplates.plone.base import get_example_file_path
from bobtemplates.plone.base import get_file_path
from bobtemplates.plone.base import get_klass_name
from bobtemplates.plone.base import get_normalized_name
from bobtemplates.plone.base import get_xml_tree
from bobtemplates.plone.base import prepare_renderer_for_subtemplate
from bobtemplates.plone.base import update_configure_zcml_include_package
from bobtemplates.plone.base import update_file


def _update_views_configure_zcml(configurator):
    file_name = u'configure.zcml'
    dir_name = u'views'

    file_path = get_file_path(configurator, file_name, dir_name)
    example_file_path = get_example_file_path(
        configurator, file_name, dir_name,
    )
    file_created = create_file_if_not_exists(file_path, example_file_path)

    if file_created:
        update_configure_zcml_include_package(
            configurator,
            package='views',
        )

    else:
        namespaces = {'browser': get_browser_namespace()}
        tree = get_xml_tree(file_path)
        tree_root = tree.getroot()

        xpath_str = "./browser:page[@name='{0}']".format(
            configurator.variables['view_name_normalized'],
        )

        if len(tree_root.xpath(xpath_str, namespaces=namespaces)):
            print(
                '{name} already in configure.zcml, skip adding!'.format(
                    name=configurator.variables['view_name_normalized'],
                ),
            )
            return

    match_str = '-*- extra stuff goes here -*-'
    insert_str = """
    <browser:page
        name="{normalized_name}"
        for="{content_type}"
        class=".views.{klass_name}View"
        temlpate="templates/{normalized_name}.pt"
        permission="{permission}"
        />

        """
    insert_str = insert_str.format(
        normalized_name=configurator.variables['view_name_normalized'],
        content_type='*',
        klass_name=configurator.variables['view_name_klass'],
        permission='zope2.View',
    )

    update_file(configurator, file_path, match_str, insert_str)
    return


def prepare_renderer(configurator):
    configurator = prepare_renderer_for_subtemplate(
        configurator,
        subtemplate='view',
    )
    view_name = configurator.variables['view_name']
    configurator.variables['view_name_klass'] = get_klass_name(view_name)
    configurator.variables['view_name_normalized'] = \
        get_normalized_name(view_name)


def post_renderer(configurator):
    _update_views_configure_zcml(configurator)
