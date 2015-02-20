Introduction
============

.. image:: https://secure.travis-ci.org/plone/bobtemplates.plone.png?branch=master
    :target: http://travis-ci.org/plone/bobtemplates.plone

.. image:: https://pypip.in/d/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Downloads

.. image:: https://pypip.in/v/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Latest Version

.. image:: https://pypip.in/egg/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Egg Status

.. image:: https://pypip.in/license/bobtemplates.plone/badge.png
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: License

``bobtemplates.plone`` provides a `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ template to generate packages for Plone projects.

To create a package like ``collective.myaddon``::

    $ mrbob -O collective.myaddon bobtemplates:plone_addon

You can also create a package with nested namespace::

    $ mrbob -O collective.foo.myaddon bobtemplates:plone_addon


Options
=======

On creating a package you can choose from the following options. The default value is in [square brackets]:


Author's name
    Should be something like 'John Smith'.

Author's email
    Should be something like 'john@plone.org'.

Author's github username
    Should be something like 'john'.

Package description [An add-on for Plone]
    One-liner describing what this package does. Should be something like 'Plone add-on that ...'.

Plone version [4.3.4]
    Which Plone version would you like to use?

Add example view? [True]
    Do you want to register a browser view 'demoview' as an example?

Add a diazo-theme? [False]
    Do you want to add a empty theme using diazo/plone.app.theming to the package?


Compatibility
=============

Addons created with ``bobtemplates.plone`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.


Installation
============

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


This creates a mrbob-executeable in your bin-directory.
Call it from the ``src``-directory of your Plone project like this.::

    $ ../bin/mrbob -O collective.foo bobtemplates:plone_addon


Installation in a virtualenv
----------------------------

You can also install ``bobtemplates.plone`` in a virtualenv.::

    $ pip install mr.bob

    $ pip install bobtemplates.plone

Now you can use it like this::

    $ mrbob -O collective.foo bobtemplates:plone_addon

See `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ documentation for further information.
