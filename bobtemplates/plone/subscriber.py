# -*- coding: utf-8 -*-

from bobtemplates.plone.base import base_prepare_renderer
from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import remove_unwanted_files
from bobtemplates.plone.base import update_configure_zcml
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort

import case_conversion as cc


def _update_package_configure_zcml(configurator):
    path = "{0}".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    match_xpath = "zope:include[@package='.subscribers']"
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".subscribers" />
"""
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _update_subscribers_configure_zcml(configurator):
    path = "{0}/subscribers".format(
        configurator.variables["package_folder"],
    )
    file_name = "configure.zcml"
    example_file_name = "{0}.example".format(file_name)
    match_xpath = "zope:subscriber[@handler='.{0}.handler']".format(
        configurator.variables["subscriber_handler_file_name"],
    )
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <subscriber for="plone.dexterity.interfaces.IDexterityContent
                   zope.lifecycleevent.interfaces.IObjectModifiedEvent"
              handler=".{0}.handler"
              />
""".format(
        configurator.variables["subscriber_handler_file_name"],
    )
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        example_file_name=example_file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _remove_unwanted_files(configurator):
    file_paths = []
    rel_file_paths = [
        "/subscribers/configure.zcml.example",
    ]
    base_path = configurator.variables["package_folder"]
    for rel_file_path in rel_file_paths:
        file_paths.append("{0}{1}".format(base_path, rel_file_path))
    remove_unwanted_files(file_paths)


def pre_renderer(configurator):
    """Pre rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "subscriber"
    name = configurator.variables["subscriber_handler_name"].strip("_")
    configurator.variables["subscriber_handler_file_name"] = cc.snakecase(name)
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_package_configure_zcml(configurator)
    _update_subscribers_configure_zcml(configurator)
    _remove_unwanted_files(configurator)
    run_black(configurator)
    run_isort(configurator)
    git_commit(
        configurator,
        "Add subscriber: {0}".format(
            configurator.variables["subscriber_handler_name"],
        ),
    )
