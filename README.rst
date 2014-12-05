Introduction
============

``bobtemplates.plone`` provides `mr.bob`_ templates to generate packages for
Plone projects.

This product is freely based on ``bobtemplates.niteoweb``.

Usage
=====

Create a mr.bob virtualenv
--------------------------

::

  mkvirtualenv mrbob

Install mr.bob and bobtemplates.plone
---------------------------------------

::

  pip install mr.bob

  pip install bobtemplates.plone

Create your package
-------------------

::

  mrbob -O collective.foo bobtemplates:plone_addon

See `mr.bob`_ documentation for further information : http://mrbob.readthedocs.org/en/latest/
