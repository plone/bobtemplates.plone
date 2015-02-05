#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render bobtemplates.plone hooks.
"""
from mrbob.bobexceptions import ValidationError

import os
import shutil
import string
import subprocess
import sys


def to_boolean(configurator, question, answer):
    """
    If you want to convert an answer to Python boolean, you can
    use this function as :ref:`post-question-hook`:

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
    """Try to get information from the git-config.
    """
    gitargs = ['git', 'config', '--get']
    try:
        result = subprocess.check_output(gitargs + [value]).strip()
        return result
    except (OSError, subprocess.CalledProcessError):
        pass


def validate_packagename(configurator):
    """Find out if the name target-dir entered when invoking the command
    can be a valid python-package.
    """
    package_dir = configurator.target_directory.split('/')[-1]
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
        msg = "Error: '{0}' is not a valid packagename.\n".format(package_dir)
        msg += "Please use a valid name (like collective.myaddon or "
        msg += "plone.app.myaddon)"
        sys.exit(msg)


def pre_username(configurator, question):
    """Get email from git and validate package name.
    """
    # validate_packagename should be run before asking the first question.
    validate_packagename(configurator)

    default = get_git_info('user.name')
    if default:
        question.default = default


def pre_email(configurator, question):
    """Get email from git.
    """
    default = get_git_info('user.email')
    if default:
        question.default = default


def post_plone_version(configurator, question, answer):
    """Find out if it is supposed to be Plone 5.
    """
    if answer.startswith('5'):
        configurator.variables['plone.is_plone5'] = True
    else:
        configurator.variables['plone.is_plone5'] = False
    return answer


def post_profile(configurator, question, answer):
    """Skip many questions if we have no profile.
    """
    value = to_boolean(configurator, question, answer)
    if not value:
        configurator.variables['package.theme'] = False
        configurator.variables['package.setuphandlers'] = False
        configurator.variables['package.testing'] = False
        configurator.variables['package.theme'] = False
        configurator.variables['travis.integration.enabled'] = False
        configurator.variables['travis.notifications.type'] = 'email'
        configurator.variables[
            'travis.notifications.destination'
        ] = 'test@plone.org'
    return value


def post_testing(configurator, question, answer):
    """Skip questions on travis if we have no profile.
    """
    value = to_boolean(configurator, question, answer)
    if not value:
        configurator.variables['travis.integration.enabled'] = False
        configurator.variables['travis.notifications.type'] = 'email'
        configurator.variables[
            'travis.notifications.destination'
        ] = 'test@plone.org'
    return value


def post_travis(configurator, question, answer):
    """Skip questions on travis.
    """
    value = to_boolean(configurator, question, answer)
    if not value:
        configurator.variables['travis.notifications.type'] = 'email'
        configurator.variables[
            'travis.notifications.destination'
        ] = 'test@plone.org'
    return value


def prepare_render(configurator):
    """Some variables to make templating easier.

    This is especially important for allowing nested and normal packages.
    """
    # get package-name and package-type from user-input
    package_dir = configurator.target_directory.split('/')[-1]
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
        dottedname = "{0}.{1}.{2}".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'])
    else:
        dottedname = "{0}.{1}".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.name'])

    # package.dottedname = 'collective.foo.something'
    configurator.variables['package.dottedname'] = dottedname

    # package.uppercasename = 'COLLECTIVE_FOO_SOMETHING'
    configurator.variables['package.uppercasename'] = configurator.variables[
        'package.dottedname'
    ].replace('.', '_').upper()

    camelcasename = dottedname.replace('.', ' ').title()\
        .replace(' ', '')\
        .replace('_', '')
    browserlayer = "{0}Layer".format(camelcasename)

    # package.browserlayer = 'CollectiveFooSomethingLayer'
    configurator.variables['package.browserlayer'] = browserlayer

    # package.longname = 'collectivefoosomething'
    configurator.variables['package.longname'] = camelcasename.lower()

    # jenkins.directories = 'collective/foo/something'
    configurator.variables[
        'jenkins.directories'
    ] = dottedname.replace('.', '/')

    # namespace_packages = "['collective', 'collective.foo']"
    if nested:
        namespace_packages = "'{0}', '{0}.{1}'".format(
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'])
    else:
        namespace_packages = "'{0}'".format(
            configurator.variables['package.namespace'])
    configurator.variables['package.namespace_packages'] = namespace_packages


def cleanup_package(configurator):
    """Cleanup and make nested if needed.

    Transform into a nested package if that was the selected option.
    Remove parts that are not needed depending on the chosen configuration.
    """

    nested = configurator.variables['package.nested']

    # construct full path '.../src/collective'
    start_path = "{0}/src/{1}".format(
        configurator.target_directory,
        configurator.variables['package.namespace'])

    # path for normal packages: '.../src/collective/myaddon'
    base_path = "{0}/{1}".format(
        start_path,
        configurator.variables['package.name'])

    if nested:
        # Event though the target-dir was 'collective.behavior.myaddon' mrbob
        # created a package collective.behavior.myaddon/src/collective/myaddon
        # since the template does not hava a folder for namespace2.
        # Here this package is turned into a nested package
        # collective.behavior.myaddon/src/collective/behavior/myaddon by
        # inserting a folder with the namepsace2 ('behavior') and oopying
        # a __init__.py into it.

        # full path for nested packages: '.../src/collective/behavior/myaddon'
        base_path_nested = "{0}/{1}/{2}".format(
            start_path,
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'])

        # directory to be created: .../src/collective/behavior
        newpath = "{0}/{1}".format(
            start_path,
            configurator.variables['package.namespace2'])
        if not os.path.exists(newpath):
            # create new directory .../src/collective/behavior
            os.makedirs(newpath)

        # copy .../src/collective/__init__.py to
        # .../src/collective/myaddon/__init__.py
        shutil.copy2("{0}/__init__.py".format(start_path), newpath)

        # move .../src/collective/myaddon to .../src/collective/behavior
        shutil.move(base_path, base_path_nested)

        # use the new path for deleting
        base_path = base_path_nested

    # find out what to delete
    to_delete = []

    if not configurator.variables['package.profile']:
        to_delete.extend([
            "{0}/profiles",
            "{0}/testing.zcml",
            "{0}/setuphandlers.py",
            "{0}/interfaces.py",
        ])

    if not configurator.variables['package.setuphandlers']:
        to_delete.extend([
            "{0}/setuphandlers.py",
        ])

    if not configurator.variables['package.locales']:
        to_delete.extend([
            "{0}/locales",
        ])

    if not configurator.variables['package.example']:
        to_delete.extend([
            "{0}/browser/templates",
            "{0}/browser/views.py",
        ])

    if not configurator.variables['package.testing']:
        to_delete.extend([
            "{0}/tests",
            "{0}/testing.py",
            "{0}/testing.zcml",
            "{0}/.coveragerc".format(configurator.target_directory),
            "{0}/buildout.d/jenkins.cfg".format(configurator.target_directory),
        ])

    if not configurator.variables['travis.integration.enabled']:
        to_delete.extend([
            "{0}/.travis.yml".format(configurator.target_directory),
            "{0}/travis.cfg".format(configurator.target_directory),
        ])

    if not configurator.variables['package.theme']:
        to_delete.extend([
            "{0}/theme",
            "{0}/profiles/default/theme.xml",
        ])

    # remove parts
    for path in to_delete:
        path = path.format(base_path)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
