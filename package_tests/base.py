# -*- coding: utf-8 -*-

import os


def init_package_base_structure(package_root):
    """creates initial folder and file structure for packages tests.
    expects: package_root
    returns: package_path
    """
    package_name = package_root.split("/")[-1]
    namespace_parts = package_name.split(".")
    package_namespace_path = "/".join(namespace_parts)
    package_path = os.path.join(package_root, u"src/" + package_namespace_path)
    profiles_path = os.path.join(package_path, u"profiles/default")
    views_path = os.path.join(package_path, u"views")
    svelte_apps_path = os.path.join(package_path, u"svelte_apps")
    theme_path = os.path.join(package_path, u"theme")
    os.makedirs(package_root)
    os.makedirs(package_path)
    os.makedirs(profiles_path)
    os.makedirs(views_path)
    os.makedirs(svelte_apps_path)
    os.makedirs(theme_path)
    template = """
[main]
version=5.1
"""
    with open(os.path.join(package_root + "/bobtemplate.cfg"), "w") as f:
        f.write(template)

    template = """
    dummy
    '-*- Extra requirements: -*-'
"""
    with open(os.path.join(package_root + "/setup.py"), "w") as f:
        f.write(template)

    template = """<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="collective.todo">

  <i18n:registerTranslations directory="locales" />

  <!--
    Be careful if you use general includeDependencies, it can have sideffects!
    Better import explicite packages or configurations ;)
  -->
  <!--<includeDependencies package="." />-->

  <include package=".views" />

</configure>
"""
    with open(os.path.join(package_path + "/configure.zcml"), "w") as f:
        f.write(template)

    template = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <version>1000</version>
  <dependencies>

  </dependencies>
</metadata>
"""
    with open(os.path.join(profiles_path + "/metadata.xml"), "w") as f:
        f.write(template)

    return package_path
