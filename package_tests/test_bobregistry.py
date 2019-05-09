# -*- coding: utf-8 -*-

from bobtemplates.eea import bobregistry


def test_reg_plone_addon():
    reg = bobregistry.plone_addon()
    assert reg.template == u'bobtemplates.eea:addon'
    assert reg.plonecli_alias == u'addon'
    assert not reg.depend_on


def test_reg_plone_buildout():
    reg = bobregistry.plone_buildout()
    assert reg.template == u'bobtemplates.eea:buildout'
    assert reg.plonecli_alias == u'buildout'
    assert not reg.depend_on


def test_reg_plone_theme_package():
    reg = bobregistry.plone_theme_package()
    assert reg.template == u'bobtemplates.eea:theme_package'
    assert reg.plonecli_alias == u'theme_package'
    assert not reg.depend_on


def test_reg_plone_theme():
    reg = bobregistry.plone_theme()
    assert reg.template == u'bobtemplates.eea:theme'
    assert reg.plonecli_alias == u'theme'
    assert reg.depend_on == 'plone_addon'


def test_reg_plone_content_type():
    reg = bobregistry.plone_content_type()
    assert reg.template == u'bobtemplates.eea:content_type'
    assert reg.plonecli_alias == u'content_type'
    assert reg.depend_on == 'plone_addon'


def test_reg_plone_behavior():
    reg = bobregistry.plone_behavior()
    assert reg.template == u'bobtemplates.eea:behavior'
    assert reg.plonecli_alias == u'behavior'
    assert reg.depend_on == 'plone_addon'


def test_reg_plone_vocabulary():
    reg = bobregistry.plone_vocabulary()
    assert reg.template == u'bobtemplates.eea:vocabulary'
    assert reg.plonecli_alias == u'vocabulary'
    assert reg.depend_on == 'plone_addon'
