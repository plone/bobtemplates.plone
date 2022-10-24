# -*- coding: utf-8 -*-

from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import git_init
from bobtemplates.plone.base import make_path
from bobtemplates.plone.utils import run_black
from bobtemplates.plone.utils import run_isort

import os
import shutil


def pre_render(configurator):
    """Some variables to make templating easier."""
    # TODO: refacture this to use base_prepare_renderer, like all sub template do
    # get package-name from user-input
    package_dir = os.path.basename(configurator.target_directory)

    namespaces = package_dir.replace("-", "_").split(".")

    configurator.variables["package.namespace"] = ".".join(namespaces[:-1])
    configurator.variables["package.dottedname"] = ".".join(namespaces)
    configurator.variables["package.name"] = namespaces[-1]

    # DISTRIBUTION NAME
    configurator.variables["package.distributionname"] = package_dir

    # package.uppercasename = 'COLLECTIVE_FOO_SOMETHING'
    configurator.variables["package.uppercasename"] = (
        configurator.variables["package.dottedname"].replace(".", "_").upper()
    )

    camelcasename = (
        configurator.variables["package.dottedname"]
        .replace(".", " ")
        .title()
        .replace(" ", "")
        .replace("_", "")
    )
    browserlayer = "{0}Layer".format(camelcasename)

    # package.browserlayer = 'CollectiveFooSomethingLayer'
    configurator.variables["package.browserlayer"] = browserlayer

    # package.longname = 'collectivefoosomething'
    configurator.variables["package.longname"] = camelcasename.lower()

    # jenkins.directories = 'collective/foo/something'
    configurator.variables["jenkins.directories"] = configurator.variables[
        "package.distributionname"
    ].replace(
        ".", "/"
    )  # NOQA: E501

    if namespaces:
        configurator.variables["package.namespace_packages"] = ", ".join(
            "'{0}'".format(".".join(namespaces[:idx]))
            for idx in range(1, len(namespaces))
        )
    else:
        configurator.variables["package.namespace_packages"] = ""


def _cleanup_package(configurator):
    """Cleanup and make nested if needed.

    Transform into a nested package if that was the selected option.
    Remove parts that are not needed depending on the chosen
    configuration.

    """

    start_path = configurator.target_directory

    if configurator.variables["package.namespace"]:
        newpath = make_path(
            start_path,
            "src",
            *configurator.variables["package.namespace"].split("."),
        )
        if not os.path.exists(newpath):
            # create new directory .../src/collective/behavior
            os.makedirs(newpath)
        oldpath = make_path(
            start_path,
            "src",
            configurator.variables["package.namespace"],
        )
        # Event though the target-dir was 'collective.behavior.myaddon' mrbob
        # created a package collective.behavior.myaddon/src/collective/myaddon
        # since the template does not hava a folder for namespace2.
        # Here this package is turned into a nested package
        # collective.behavior.myaddon/src/collective/behavior/myaddon by
        # inserting a folder with the namepsace2 ('behavior') and copying
        # a __init__.py into it.
        if oldpath != newpath:
            # move .../src/collective/myaddon to .../src/collective/behavior
            if not os.path.exists(
                make_path(newpath, configurator.variables["package.name"])
            ):
                shutil.move(
                    make_path(oldpath, configurator.variables["package.name"]), newpath
                )
            init = make_path(oldpath, "__init__.py")
            namespaces = configurator.variables["package.namespace"].split(".")
            for idx in range(len(namespaces)):
                shutil.copy(init, make_path(start_path, "src", *namespaces[: idx + 1]))
            shutil.rmtree(oldpath)


def pre_ask(configurator):
    """ """


def post_render(configurator):
    _cleanup_package(configurator)
    run_isort(configurator)
    run_black(configurator)
    git_init_status = git_init(configurator)
    if git_init_status:
        git_commit(
            configurator,
            "Create addon: {0}".format(
                configurator.variables["package.dottedname"],
            ),
        )
