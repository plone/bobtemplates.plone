Introduction
============

``bobtemplates.plone`` provides a `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ template to generate packages for Plone projects.

To create a package like ``collective.myaddon``

.. code-block:: console

    $ pip install bobtemplates.plone
    $ mrbob -O collective.myaddon bobtemplates:plone_addon

You can also create a package with nested namespace

.. code-block:: console

    $ mrbob -O collective.foo.myaddon bobtemplates:plone_addon


Options
-------

On creating a package you can choose from the following options. The default value is in [square brackets]:

Package Type? [Basic]
    Options are Basic, Dexterity and Theme.

Author's name
    Should be something like 'John Smith'.

Author's email
    Should be something like 'john@plone.org'.

Author's github username
    Should be something like 'john'.

Package description [An add-on for Plone]
    One-liner describing what this package does. Should be something like 'Plone add-on that ...'.

Plone version [5.0.6]
    Which Plone version would you like to use?


Features
--------

Package created with ``bobtemplates.plone`` use the current best-practices when creating an add-on.

Buildout
    The package is contained in a buildout that allows you to build Plone with the new package installed for testing-purposes.

Tests
    The package comes with a test setup and some `tests <http://docs.plone.org/external/plone.app.testing/docs/source/index.html>`_ for installing the package. It also contains a `robot-test <http://docs.plone.org/external/plone.app.robotframework/docs/source/index.html>`_ that tests logging in. The buildout also contains a config to allow testing the package on `travis <http://travis-ci.org/>`_ that sends `notifications <http://about.travis-ci.org/docs/user/notifications>`_ by email to the package author.

Profile
    The package contains a `Generic Setup Profile <http://docs.plone.org/develop/addons/components/genericsetup.html>`_ that installs a browserlayer. For Plone 5 it also contains a uninstall-profile.

Locales
    The package registers a directory for locales.

Template-Overrides
    The package registers the folder ``browser/overrides`` as a directory where you can drop template-overrides using `z3c.jbot <https://pypi.python.org/pypi/z3c.jbot>`_.

Setuphandler
    The package contains a `setuphandlers.py <http://docs.plone.org/develop/addons/components/genericsetup.html?highlight=setuphandler#custom-installer-code-setuphandlers-py>`_ where you can add code that is executed on installing the package. For Plone 5 there is also a method in `setuphandler.py` that is run on uninstalling.

The package-types `Dexterity` and `Theme` add the following to `Basic`:

Dexterity
    Adds a simple content-type (you get asked about its name) in ``profiles/default/types/`` with a python-schema in ``interfaces.py``.

Theme
    Adds a simple bootstrap-based Diazo theme in the folder ``theme/`` and registers it in ``profiles/default/theme.xml``


See `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ documentation for further information.
