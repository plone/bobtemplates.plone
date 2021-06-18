# -*- coding: utf-8 -*-

import case_conversion as cc

from bobtemplates.plone.base import (
    base_prepare_renderer,
    git_commit,
    remove_unwanted_files,
    update_configure_zcml,
)
from bobtemplates.plone.utils import run_black, run_isort


def _update_package_configure_zcml(configurator):
    path = "{0}".format(
        configurator.variables["package_folder"],
    )
    file_name = u"configure.zcml"
    match_xpath = "zope:include[@package='.indexers']"
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include package=".indexers" />
"""
    update_configure_zcml(
        configurator,
        path,
        file_name=file_name,
        match_xpath=match_xpath,
        match_str=match_str,
        insert_str=insert_str,
    )


def _update_indexers_configure_zcml(configurator):
    path = "{0}/indexers".format(
        configurator.variables["package_folder"],
    )
    file_name = u"configure.zcml"
    example_file_name = "{0}.example".format(file_name)
    match_xpath = "zope:include[@package='.{0}']".format(
        configurator.variables["indexer_name"]
    )
    match_str = "-*- extra stuff goes here -*-"
    insert_str = """
  <include file="{0}.zcml" />
""".format(
        configurator.variables["indexer_name"]
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
        "/indexers/configure.zcml.example",
    ]
    base_path = configurator.variables["package_folder"]
    for rel_file_path in rel_file_paths:
        file_paths.append("{0}{1}".format(base_path, rel_file_path))
    remove_unwanted_files(file_paths)


def pre_renderer(configurator):
    """Pre rendering."""
    configurator = base_prepare_renderer(configurator)
    configurator.variables["template_id"] = "indexer"
    name = configurator.variables["indexer_name"].strip("_")
    indexer_name = cc.snakecase(name)
    configurator.variables["indexer_name"] = indexer_name
    configurator.variables["indexer_file_name"] = indexer_name
    configurator.target_directory = configurator.variables["package_folder"]


def post_renderer(configurator):
    """Post rendering."""
    _update_package_configure_zcml(configurator)
    _update_indexers_configure_zcml(configurator)
    _remove_unwanted_files(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_commit(
        configurator,
        "Add indexer: {0}".format(
            configurator.variables["indexer_name"],
        ),
    )
