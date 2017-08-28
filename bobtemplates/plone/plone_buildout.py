# -*- coding: utf-8 -*-

from bobtemplates.plone.subcommand import logger


def prepare_renderer(configurator):
    configurator.variables['template_id'] = 'plone_buildout'
    logger.info("Using plone_buildout template:".format(
        configurator.variables['template_id']))


def post_renderer(configurator):
    """
    """
