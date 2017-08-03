# -*- coding: utf-8 -*-

from mrbob.bobexceptions import ValidationError
from bobtemplates.plone.subcommand import base_prepare_renderer
from bobtemplates.plone.subcommand import logger
import re


def post_theme_name(configurator, question, answer):
    regex = r'^\w+[a-zA-Z0-9 \.\-_]*\w$'
    if not re.match(regex, answer):
        msg = u"Error: '{0}' is not a valid themename.\n".format(answer)
        msg += u"Please use a valid name (like 'Tango' or 'my-tango.com')!\n"
        msg += u"At beginning or end only letters|diggits are allowed.\n"
        msg += u"Inside the name also '.-_' are allowed.\n"
        msg += u"No umlauts!"
        raise ValidationError(msg)
    return answer


def prepare_renderer(configurator):
    logger.info("Using plone_theme template:")
    configurator = base_prepare_renderer(configurator)
    configurator.variables['template_id'] = 'plone_theme'

    # TODO: update buildout config


def post_renderer(configurator):
    """
    """
