Introduction
============

``bobtemplates.plone`` provides `mr.bob`_ templates to generate packages for
Plone projects.

It is based on `bobtemplates.niteoweb <https://github.com/niteoweb/bobtemplates.niteoweb>`_ and `bobtemplates.ecreall <https://github.com/cedricmessiant/bobtemplates.ecreall>`_


Options
=======

This package provided two templaes to be used with Plone:

plone_addon
    A Plone addon like ``collective.myaddon``

plone_addon_nested
    A Plone with nested namespaces like ``collective.behavior.myaddon``


On creating a package the templates let you choose from the following options:

Namespace of the package
    Should be something like 'plone' or 'collective'.

Namespace of the package (part 2)
    Should be something like 'app'. (Only for the template plone_addon_nested)

Name of the package
    Should be something like 'myaddon'.

Package description
    One-liner describing what this package does. Should be something like 'Plone add-on that ...'.

Package keywords
    Keywords/categoris describing this package. Should be something like 'Plone Python Diazo...'.

Version of the package [0.1]
    Should be something like '0.1'.

License of the package [GPL]
    Should be something like 'GPL'.

Author's name
    Should be something like 'John Smith'.

Author's email
    Should be something like 'john@plone.org'.

Author's github username
    Should be something like 'john'.

Plone version [4.3.4]
    Which Plone version would you like to use?

Python version [2.7]
    Which Python version would you like to use?

Use grok? [False]
    Do you want to use grok in the package?

Add locales? [False]
    Do you want to add translations to this package?

Use generic setup profile? [True]
    Do you want the package to have a generic setup profile? If you select False all following questions will be skipped.

Add setuphandlers? [True]
    Do you want the package to have a setuphander.py to run cusotm code during install?

Add a diazo-theme? [False]
    Do you want to add a empty theme using diazo/plone.app.theming to the package?

Add tests? [True]
    Do you want to add a basic setup for tests, robot-tests and travis-integration?

Prepare Travis Integration? [False]
    Should the package be prepared to be integrated into travis (http://travis-ci.org)? If you select False all following questions will be skipped.

Type of Travis CI notifications [email]
    Should be something like 'email' or 'irc', see : http://about.travis-ci.org/docs/user/notifications for more information.

Destination for Travis CI notifications
    Should be something like 'travis-reports@example.com' or 'irc.freenode.org#plone'.


Use in a buildout
-----------------

::

    [buildout]
    parts += mrbob

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.plone

    [sources]
    # if you want to make local changes on the templates
    bobtemplates.plone = git https://github.com/collective/bobtemplates.plone.git pushurl=git@github.com:collective/bobtemplates.plone.git


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

.. _mr.bob: http://mrbob.readthedocs.org/en/latest/
