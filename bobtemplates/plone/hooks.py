#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render bobtemplates.plone hooks.

DEPRECATED, dont't use this and don't add new stuff here please!

"""
from bobtemplates.plone.base import _set_plone_version_variables
from mrbob.bobexceptions import ValidationError

import os
import shutil
import string
import subprocess
import sys


def to_boolean(configurator, question, answer):
    """If you want to convert an answer to Python boolean, you can use this
    function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        idiot.question = Are you young?
        idiot.post_ask_question = mrbob.hooks:to_boolean

    Following variables can be converted to a boolean:
    **y, n, yes, no, true, false, 1, 0**

    """
    if isinstance(answer, bool):
        return answer
    value = answer.lower()
    if value in ['y', 'yes', 'true', '1']:
        return True
    elif value in ['n', 'no', 'false', '0']:
        return False
    else:
        raise ValidationError('Value must be a boolean (y/n)')


def get_git_info(value):
    """Try to get information from the git-config."""
    gitargs = ['git', 'config', '--get']
    try:
        result = subprocess.check_output(gitargs + [value]).strip()
        return result
    except (OSError, subprocess.CalledProcessError):
        pass


def validate_packagename(configurator):
    """Find out if the name target-dir entered when invoking the command can be
    a valid python-package."""
    package_dir = os.path.basename(configurator.target_directory)
    fail = False

    allowed = set(string.ascii_letters + string.digits + '.-_')
    if not set(package_dir).issubset(allowed):
        fail = True

    if package_dir.startswith('.') or package_dir.endswith('.'):
        fail = True

    parts = len(package_dir.split('.'))
    if parts < 2 or parts > 3:
        fail = True

    if fail:
        msg = (
            "Error: '{0}' is not a valid packagename.\n"
            'Please use a valid name (like collective.myaddon or '
            'plone.app.myaddon)'.format(package_dir)
        )
        sys.exit(msg)


def pre_username(configurator, question):
    """Get email from git and validate package name."""
    # validate_packagename should be run before asking the first question.
    validate_packagename(configurator)

    default = get_git_info('user.name')
    if default:
        question.default = default


def pre_email(configurator, question):
    """Get email from git."""
    default = get_git_info('user.email')
    if default:
        question.default = default


def post_plone_version(configurator, question, answer):
    """Find out if it is supposed to be Plone 5."""
    _set_plone_version_variables(configurator, answer)
    return answer


def prepare_render(configurator):
    """Some variables to make templating easier.

    This is especially important for allowing nested and normal
    packages.

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


def cleanup_package(configurator):
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


def make_path(*args):
    """generate path string."""
    return os.sep.join(args)
