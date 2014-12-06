#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Render bobtemplates.plone hooks.
"""
from mrbob.bobexceptions import ValidationError

import os
import shutil


def to_boolean(configurator, question, answer):
    """
    If you want to convert an answer to Python boolean, you can
    use this function as :ref:`post-question-hook`:

    .. code-block:: ini

        [questions]
        idiot.question = Are you young?
        idiot.post_ask_question = mrbob.hooks:to_boolean

    Following variables can be converted to a boolean: **y, n, yes, no, true, false, 1, 0**
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


def suggest_namespace(configurator, question):
    package_dir = configurator.target_directory.split('/')[-1]
    namespace = package_dir.split('.')[0]
    question.default = namespace


def suggest_namespace2(configurator, question):
    package_dir = configurator.target_directory.split('/')[-1]
    namespace2 = package_dir.split('.')[1]
    question.default = namespace2


def suggest_name(configurator, question):
    package_dir = configurator.target_directory.split('/')[-1]
    name = package_dir.split('.')[-1]
    question.default = name


def post_profile(configurator, question, answer):
    """ Skip many questions if we have no profile.
    """
    value = to_boolean(configurator, question, answer)
    if not value:
        configurator.variables['package.theme'] = False
        configurator.variables['package.setuphandlers'] = False
        configurator.variables['package.testing'] = False
        configurator.variables['package.theme'] = False
        configurator.variables['travis.integration.enabled'] = False
        configurator.variables['travis.notifications.destination'] = False
        configurator.variables['travis.notifications.type'] = False
    return value


def post_testing(configurator, question, answer):
    """ Skip questions on travis if we have no profile.
    """
    value = to_boolean(configurator, question, answer)
    if not value:
        configurator.variables['travis.integration.enabled'] = False
        configurator.variables['travis.notifications.destination'] = False
        configurator.variables['travis.notifications.type'] = False
    return value


def post_travis(configurator, question, answer):
    """ Skip questions on travis.
    """
    value = to_boolean(configurator, question, answer)
    if not value:
        configurator.variables['travis.notifications.type'] = 'email'
        configurator.variables['travis.notifications.destination'] = 'test@plone.org'
    return value


def cleanup_package(configurator):
    """ Remove parts that are not needed depending on the chosen configuration.
    """

    to_delete = []

    base_path = "{0}/src/{1}/{2}".format(
        configurator.target_directory,
        configurator.variables['package.namespace'],
        configurator.variables['package.name'])

    if configurator.template_dir.endswith('plone_addon_nested'):
        base_path = "{0}/src/{1}/{2}/{3}".format(
            configurator.target_directory,
            configurator.variables['package.namespace'],
            configurator.variables['package.namespace2'],
            configurator.variables['package.name'])

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
            "{0}/.travis.yml",
            "{0}/travis.cfg",
            "{0}/.coveragerc",
            "{0}/profile/testing",
        ])

    if not configurator.variables['travis.integration.enabled']:
        to_delete.extend([
            "{0}/.travis.yml",
            "{0}/travis.cfg",
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
