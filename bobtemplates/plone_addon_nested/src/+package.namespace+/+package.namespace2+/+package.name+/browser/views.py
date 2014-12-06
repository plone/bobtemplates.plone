# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from plone import api

import logging
logger = logging.getLogger(__name__)


class DemoView(BrowserView):
    """ This is a sample browser view with one method.
    """

    def get_types(self):
        """Returns a dict with type names and the amount of items
        for this type in the site.
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_types = api.portal.get_tool('portal_types')
        content_types = portal_types.listContentTypes()
        results = []
        for ct in content_types:
            brains = portal_catalog(portal_type=ct)
            if brains:
                results.append({
                    'type': ct,
                    'qtt': len(brains),
                })
            else:
                logger.info("No elements of type {0}".format(ct))

        return results
