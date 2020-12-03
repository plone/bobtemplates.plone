# -*- coding: utf-8 -*-

from bobtemplates.eea.base import git_commit
from bobtemplates.eea.base import git_init
from bobtemplates.eea.base import make_path

import os
import shutil


def pre_render(configurator):
    """Some variables to make templating easier.
    """
    # get package-name from user-input
    package_dir = os.path.basename(configurator.target_directory)
    nested = bool(len(package_dir.split('.')) == 3)
    configurator.variables['package.nested'] = nested
    configurator.variables['package.namespace'] = package_dir.split('.')[0]
    if nested:
        namespace2 = package_dir.split('.')[1]
    else:
        # in order for it to work with the 3 namespace template we use the
        # first namespace as placeholder
        namespace2 = configurator.variables['package.namespace']
    configurator.variables['package.namespace2'] = namespace2
    configurator.variables['package.name'] = package_dir.split('.')[-1]

    if nested:
        dottedname = '{0}.{1}.{2}'.format(
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'],
        )
    else:
        dottedname = '{0}.{1}'.format(
            configurator.variables['package.namespace'],
            configurator.variables['package.name'],
        )

    # package.dottedname = 'collective.foo.something'
    configurator.variables['package.dottedname'] = dottedname

    # package.uppercasename = 'COLLECTIVE_FOO_SOMETHING'
    configurator.variables['package.uppercasename'] = \
        configurator.variables['package.dottedname'].replace('.', '_').upper()

    camelcasename = dottedname.replace('.', ' ').title()\
        .replace(' ', '')\
        .replace('_', '')
    browserlayer = '{0}Layer'.format(camelcasename)

    # package.browserlayer = 'CollectiveFooSomethingLayer'
    configurator.variables['package.browserlayer'] = browserlayer

    # package.longname = 'collectivefoosomething'
    configurator.variables['package.longname'] = camelcasename.lower()

    # jenkins.directories = 'collective/foo/something'
    configurator.variables['jenkins.directories'] = dottedname.replace('.', '/')  # NOQA: E501

    # namespace_packages = "['collective', 'collective.foo']"
    if nested:
        namespace_packages = "'{0}', '{0}.{1}'".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'],
        )
    else:
        namespace_packages = "'{0}'".format(
            configurator.variables['package.namespace'],
        )
    configurator.variables['package.namespace_packages'] = namespace_packages


def _cleanup_package(configurator):
    """Cleanup and make nested if needed.

    Transform into a nested package if that was the selected option.
    Remove parts that are not needed depending on the chosen
    configuration.

    """
    nested = configurator.variables['package.nested']

    # construct full path '.../src/collective'
    start_path = make_path(
        configurator.target_directory,
        configurator.variables['package.namespace'],
    )

    # path for normal packages: '.../src/collective/myaddon'
    base_path = make_path(
        start_path,
        configurator.variables['package.name'],
    )

    if nested:
        # full path for nested packages
        base_path_nested = make_path(
            start_path,
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'],
        )

        # delete base path folder if it exists since it is not required
        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        # use the new path for deleting
        base_path = base_path_nested
    else:
        base_path_nested = make_path(
            start_path,
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'],
        )

        # mkdir base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # move files/folders from base_path_nested in base_path
        for file in os.listdir(base_path_nested):
            path = make_path(base_path_nested, file)
            newpath = make_path(base_path, file)
            shutil.move(path, newpath)

        newpath = make_path(
            start_path,
            configurator.variables['package.namespace2'],
        )
        # delete the extra placeholder folder
        shutil.rmtree(newpath)


def pre_ask(configurator):
    """
    """


def post_render(configurator):
    _cleanup_package(configurator)
    git_init_status = git_init(configurator)
    if git_init_status:
        git_commit(
            configurator,
            'Create addon: {0}'.format(
                configurator.variables['package.dottedname'],
            ),
        )
