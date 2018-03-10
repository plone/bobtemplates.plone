# -*- coding: utf-8 -*-

from operator import itemgetter
from Products.Five.browser import BrowserView


class DemoView(BrowserView):
    def the_title(self):
        return u'A list of talks:'

    def talks(self,):
        results = []
        data = [{'title': 'Dexterity is the new default!',
                 'subjects': ('content-types', 'dexterity')},
                {'title': 'Mosaic will be the next big thing.',
                 'subjects': ('layout', 'deco', 'views'),
                 'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                {'title': 'The State of Plone', 'subjects': ('keynote',)},
                {'title': 'Diazo is a powerful tool for theming!',
                 'subjects': ('design', 'diazo', 'xslt')},
                ]
        for item in data:
            try:
                url = item['url']
            except KeyError:
                url = 'https://www.google.com/search?q=%s' % item['title']
            talk = dict(
                title=item['title'],
                subjects=', '.join(item['subjects']),
                url=url
            )
            results.append(talk)
        return sorted(results, key=itemgetter('title'))
