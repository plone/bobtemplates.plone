# -*- coding: utf-8 -*-

from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import git_init

import os


def pre_render(configurator):
    """ using addon method """
    package_dir = os.path.basename(configurator.target_directory)

    configurator.variables["template_id"] = "addon_resources"

    configurator.variables["package.namespace"] = package_dir.split(".")[0]
    configurator.variables["package.name"] = package_dir.split(".")[-1]

    dottedname = "{0}.{1}".format(
        configurator.variables["package.namespace"],
        configurator.variables["package.name"],
    )

    # package.dottedname = 'collective.foo.something'
    configurator.variables["package.dottedname"] = dottedname


def post_render(configurator):
    """ using addon method """
    git_init_status = git_init(configurator)
    if git_init_status:
        git_commit(
            configurator,
            "Create addon: {0}".format(configurator.variables["package.dottedname"]),
        )
