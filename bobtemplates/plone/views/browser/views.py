""" Example view
"""

# Zope imports
from zope.interface import Interface
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyView(BrowserView):
    """ Render the title and description of item only (example)
    """
    index = ViewPageTemplateFile("myview.pt")