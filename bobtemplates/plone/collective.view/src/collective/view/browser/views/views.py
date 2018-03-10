# -*- coding: utf-8 -*-

from operator import itemgetter
from Products.Five.browser import BrowserView


class DemoView(BrowserView):
    def the_title(self):
        return u'A list of talks:'

    def talks(self):
        results = []
        data = [{'title': 'Dexter'}, {'title': 'Plone'}]
        for item in data:
            try:
                url = item['url']
            except KeyError:
                url = 'google.com'
            talk = dict(
                title=item['title'],
                subjects=', '.join(item['subjects']),
                url=url
            )
            results.append(talk)
        return sorted(results, key=itemgetter('title'))
