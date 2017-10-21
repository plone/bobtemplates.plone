# -*- coding: utf-8 -*-


class RegEntry(object):
    def __init__(self):
        self.template = ''
        self.plonecli_alias = ''
        self.depend_on = None


def plone_addon():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:addon'
    reg.plonecli_alias = 'addon'
    return reg


def plone_buildout():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:buildout'
    reg.plonecli_alias = 'buildout'
    return reg


def plone_theme_package():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:theme_package'
    reg.plonecli_alias = 'theme_package'
    return reg


def plone_theme():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:theme'
    reg.plonecli_alias = 'theme'
    reg.depend_on = 'plone_addon'
    return reg


def plone_content_type():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:content_type'
    reg.plonecli_alias = 'content_type'
    reg.depend_on = 'plone_addon'
    return reg


def plone_vocabulary():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:vocabulary'
    reg.plonecli_alias = 'vocabulary'
    reg.depend_on = 'plone_addon'
    return reg
