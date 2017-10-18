# -*- coding: utf-8 -*-


class RegEntry(object):
    def __init__(self):
        self.template = ''
        self.depend_on = None


def plone_addon():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:addon'
    return reg


def plone_buildout():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:buildout'
    return reg


def plone_theme_package():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:theme_package'
    return reg


def theme():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:theme'
    reg.depend_on = 'plone_addon'
    return reg


def content_type():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:content_type'
    reg.depend_on = 'plone_addon'
    return reg


def vocabulary():
    reg = RegEntry()
    reg.template = 'bobtemplates.plone:vocabulary'
    reg.depend_on = 'plone_addon'
    return reg
