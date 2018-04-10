# -*- coding: utf-8 -*-

from bobtemplates.plone.base import git_commit
from bobtemplates.plone.base import git_init
from bobtemplates.plone.base import make_path

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
        namespace2 = None
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

    if configurator.variables.get('theme.name'):
        def normalize_string(value):
            value = '-'.join(value.split('_'))
            value = '-'.join(value.split())
            return value
        configurator.variables['theme.normalized_name'] = normalize_string(
            configurator.variables.get('theme.name'),
        ).lower()
    else:
        configurator.variables['theme.normalized_name'] = ''


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
        'src',
        configurator.variables['package.namespace'],
    )

    # path for normal packages: '.../src/collective/myaddon'
    base_path = make_path(
        start_path,
        configurator.variables['package.name'],
    )

    if nested:
        # Event though the target-dir was 'collective.behavior.myaddon' mrbob
        # created a package collective.behavior.myaddon/src/collective/myaddon
        # since the template does not hava a folder for namespace2.
        # Here this package is turned into a nested package
        # collective.behavior.myaddon/src/collective/behavior/myaddon by
        # inserting a folder with the namepsace2 ('behavior') and oopying
        # a __init__.py into it.

        # full path for nested packages: '.../src/collective/behavior/myaddon'
        base_path_nested = make_path(
            start_path,
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'],
        )

        # directory to be created: .../src/collective/behavior
        newpath = make_path(
            start_path,
            configurator.variables['package.namespace2'],
        )
        if not os.path.exists(newpath):
            # create new directory .../src/collective/behavior
            os.makedirs(newpath)

        # copy .../src/collective/__init__.py to
        # .../src/collective/myaddon/__init__.py
        init = make_path(start_path, '__init__.py')
        shutil.copy2(init, newpath)

        # move .../src/collective/myaddon to .../src/collective/behavior
        shutil.move(base_path, base_path_nested)

        # use the new path for deleting
        base_path = base_path_nested

    # find out what to delete
    to_delete = []

    # remove parts
    for path in to_delete:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


def pre_ask(configurator):
    """
    """


def post_render(configurator):
    _cleanup_package(configurator)
    if configurator.variables.get('package.git.init'):
        git_init(configurator)
    git_commit(
        configurator,
        'Create theme_package: {0}'.format(
            configurator.variables['package.dottedname'],
        ),
    )
