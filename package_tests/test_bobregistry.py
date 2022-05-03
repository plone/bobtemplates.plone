# -*- coding: utf-8 -*-

from bobtemplates.plone import bobregistry


def test_reg_plone_addon():
    reg = bobregistry.plone_addon()
    assert reg.template == "bobtemplates.plone:addon"
    assert reg.plonecli_alias == "addon"
    assert not reg.depend_on


def test_reg_plone_buildout():
    reg = bobregistry.plone_buildout()
    assert reg.template == "bobtemplates.plone:buildout"
    assert reg.plonecli_alias == "buildout"
    assert not reg.depend_on


def test_reg_plone_theme():
    reg = bobregistry.plone_theme()
    assert reg.template == "bobtemplates.plone:theme"
    assert reg.plonecli_alias == "theme"
    assert reg.depend_on == "plone_addon"


def test_reg_plone_content_type():
    reg = bobregistry.plone_content_type()
    assert reg.template == "bobtemplates.plone:content_type"
    assert reg.plonecli_alias == "content_type"
    assert reg.depend_on == "plone_addon"


def test_reg_plone_behavior():
    reg = bobregistry.plone_behavior()
    assert reg.template == "bobtemplates.plone:behavior"
    assert reg.plonecli_alias == "behavior"
    assert reg.depend_on == "plone_addon"


def test_reg_plone_vocabulary():
    reg = bobregistry.plone_vocabulary()
    assert reg.template == "bobtemplates.plone:vocabulary"
    assert reg.plonecli_alias == "vocabulary"
    assert reg.depend_on == "plone_addon"
