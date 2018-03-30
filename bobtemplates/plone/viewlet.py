# -*- coding: utf-8 -*-
from bobtemplates.plone.base import create_file_if_not_exists
from bobtemplates.plone.base import get_example_file_path
from bobtemplates.plone.base import get_file_path
from bobtemplates.plone.base import get_klass_name
from bobtemplates.plone.base import get_normalized_name
from bobtemplates.plone.base import prepare_renderer_for_subtemplate
from bobtemplates.plone.base import update_file


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

    match_str = '-*- extra stuff goes here -*-'
    insert_str = """
    <browser:viewlet
        name="{normalized_name}"
        for="{content_type}"
        manager="plone.app.layout.viewlets.interfaces.I{manager}"
        class=".viewlets.{klass_name}Viewlet"
        layer={layer}
        temlpate="templates/{normalized_name}.pt"
        permission="{permission}"
        />

        """
    insert_str = insert_str.format(
        normalized_name=configurator.variables['view_name_normalized'],
        content_type='*',
        manager=configurator.variables['manager_name_klass'],
        klass_name=configurator.variables['view_name_klass'],
        layer='zope.interface.Interface',
        permission='zope2.View',
    )

    update_file(configurator, file_path, match_str, insert_str)
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
