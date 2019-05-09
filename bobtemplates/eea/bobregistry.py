# -*- coding: utf-8 -*-


class RegEntry(object):
    def __init__(self):
        self.template = ''
        self.plonecli_alias = ''
        self.depend_on = None
        self.deprecated = False
        self.info = ''


def plone_addon():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:addon'
    reg.plonecli_alias = 'addon'
    return reg


def plone_buildout():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:buildout'
    reg.plonecli_alias = 'buildout'
    return reg


def plone_theme_package():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:theme_package'
    reg.plonecli_alias = 'theme_package'
    reg.deprecated = True
    reg.info = """Please use the theme_barceloneta subtemplate!
    """
    return reg


def plone_theme():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:theme'
    reg.plonecli_alias = 'theme'
    reg.depend_on = 'plone_addon'
    return reg


def plone_theme_barceloneta():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:theme_barceloneta'
    reg.plonecli_alias = 'theme_barceloneta'
    reg.depend_on = 'plone_addon'
    return reg


def plone_content_type():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:content_type'
    reg.plonecli_alias = 'content_type'
    reg.depend_on = 'plone_addon'
    return reg


def plone_view():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:view'
    reg.plonecli_alias = 'view'
    reg.depend_on = 'plone_addon'
    return reg


def plone_portlet():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:portlet'
    reg.plonecli_alias = 'portlet'
    reg.depend_on = 'plone_addon'
    return reg


def plone_viewlet():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:viewlet'
    reg.plonecli_alias = 'viewlet'
    reg.depend_on = 'plone_addon'
    return reg


def plone_vocabulary():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:vocabulary'
    reg.plonecli_alias = 'vocabulary'
    reg.depend_on = 'plone_addon'
    return reg


def plone_behavior():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:behavior'
    reg.plonecli_alias = 'behavior'
    reg.depend_on = 'plone_addon'
    return reg


def plone_restapi_service():
    reg = RegEntry()
    reg.template = 'bobtemplates.eea:restapi_service'
    reg.plonecli_alias = 'restapi_service'
    reg.depend_on = 'plone_addon'
    return reg
