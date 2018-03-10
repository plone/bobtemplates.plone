# -*- coding: utf-8 -*-


from bobtemplates.plone import base
from bobtemplates.plone import view
from mrbob.configurator import Configurator


def test_prepare_renderer():
    configurator = Configurator(
        template='bobtemplates.plone:view',
        target_directory='collective.foo.bar',
        variables={
            'view_name': 'Talks',
        },
    )

    view.prepare_renderer(configurator)

    variables = [
        'view_name',
        'view_name_klass',
        'view_name_normalized',
    ]
    for variable in variables:
        assert variable in configurator.variables

    return


def test_post_renderer(tmpdir):
    import os

    target_path = tmpdir.strpath + '/collective.todo'
    package_path = target_path + '/src/collective/todo'
    browser_path = package_path + '/browser'

    os.makedirs(target_path)
    os.makedirs(package_path)
    os.makedirs(browser_path)

    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

</configure>
"""
    with open(browser_path + '/configure.zcml', 'w') as f:
        f.write(template)

    template = """# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
# -*- Extra imports go here -*-


# -*- Extra views go here -*-
"""
    with open(browser_path + '/views.py', 'w') as f:
        f.write(template)

    template = """
[tool:bobtemplates.plone]
version=5.1
"""
    with open(os.path.join(target_path + '/setup.cfg'), 'w') as f:
        f.write(template)

    template = """
    dummy
    '-*- Extra requirements: -*-'
"""
    with open(os.path.join(target_path + '/setup.py'), 'w') as f:
        f.write(template)

    configurator = Configurator(
        template='bobtemplates.plone:addon',
        target_directory=package_path,
        variables={
            'view_name': 'Talks',
            'plone.version': '5.1',
            'description': 'A list of Talks',
            'title': 'Talks',
        },
    )

    os.chdir(package_path)
    base.set_global_vars(configurator)
    view.prepare_renderer(configurator)
    view.post_renderer(configurator)

    return
