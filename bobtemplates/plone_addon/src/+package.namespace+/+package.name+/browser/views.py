# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from plone import api

import logging
logger = logging.getLogger(__name__)


class DemoView(BrowserView):
    """ This does nothing so far
    """

    def get_types(self):
        catalog_tool = api.portal.get_tool('portal_catalog')
        types_tool = api.portal.get_tool('portal_types')

        results = []
        content_types = types_tool.listContentTypes()

        for ct in content_types:
            qtt = len(catalog_tool(portal_type=ct))
            if qtt > 0:
                results.append({'type': ct, 'qtt': qtt, })

        return results
