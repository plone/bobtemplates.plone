Introduction
============

``bobtemplates.plone`` provides `mr.bob`_ templates to generate packages for
Plone projects.

This product is based on ``bobtemplates.niteoweb`` and ``bobtemplates.ecreall``.

Usage
=====

Options:

* create a theme

Use in a buildout
-----------------

Use this option until the package was released on pypi.

::

    [buildout]
    parts += mrbob

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.plone

    [sources]
    bobtemplates.plone = git git@github.com:starzel/bobtemplates.plone.git


In the ``src``-directory of your Plone project do:

::

    ../bin/mrbob -O collective.foo bobtemplates:plone_addon



Create a mr.bob virtualenv
--------------------------

Alternatively you can install the package in your virtualenv.

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
