
.. image:: https://secure.travis-ci.org/plone/bobtemplates.plone.png?branch=master
    :target: http://travis-ci.org/plone/bobtemplates.plone

.. image:: https://coveralls.io/repos/github/plone/bobtemplates.plone/badge.svg?branch=master
    :target: https://coveralls.io/github/plone/bobtemplates.plone?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/dm/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/l/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: License

bobtemplates.plone
==================

``bobtemplates.plone`` provides a `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ template to generate packages for Plone projects.


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
    Adds the Default Plone 5 theme Barceloneta in the folder ``theme/`` and registers it in ``profiles/default/theme.xml``


Compatibility
=============

Add-ons created with ``bobtemplates.plone`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.
It should work on Linux, Mac and Windows.


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.

It is also available online at http://docs.plone.org/develop/addons/bobtemplates.plone/bobtemplates.plone/README.html

Installation
------------

Python Package Managers
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    # use a virtual environment for installation

    # For Python 2 and before Python 3.4 use:
    $ virtualenv <path_venv>

    # For Python 3.4 and above use:
    $ python -m venv <path_venv>

    # Activate your virtual environment
    $ source <path_venv>/bin/activate

    # Install bobtemplates.plone
    $ pip install bobtemplates.plone


Via a buildout
^^^^^^^^^^^^^^

.. code-block:: ini

    [buildout]
    parts += mrbob

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.plone

Usage
-----

Both installation ways creates a mrbob-executable in your bin-directory.
Call it from the ``src``-directory of your Plone project like this:

.. code-block:: console

    $ ../bin/mrbob -O collective.foo bobtemplates:plone_addon

Or to create a new theme package:

.. code-block:: console

    $ mrbob -O plonetheme.bar bobtemplates:plone_theme_package

Or to create a new fattheme buildout:

.. code-block:: console

    $ mrbob -O myfatbuildout bobtemplates:plone_fattheme_buildout

Contribute
----------

- Issue Tracker: https://github.com/plone/bobtemplates.plone/issues
- Source Code: https://github.com/plone/bobtemplates.plone
- Documentation: http://docs.plone.org/develop/addons/bobtemplates.plone/bobtemplates.plone/README.html

This package should follow best practices, or even define them, therefore it might feels uncommon for normal Plone development to contribute.
bobtemplates.plone is changed to be as pythonic as possible, also in its way to contribute and test.

We do use `tox <http://tox.readthedocs.io/en/latest/>`_ as test invocation tool.
This package itself did not provide any buildout or other Plone typical method.
It uses pytest as test framework.


Development
^^^^^^^^^^^

If you want to contribute, please check out this repository, apply your changes and make a pull request.
It would be good if you run test, especially the code convention tests before submitting a pull request, see following sections.

You do not need to install any additional elements or run a buildout.
Tox will take care for everything additional.

Running tests
^^^^^^^^^^^^^

You need tox installed somewhere and available in your path, nothing else is neccessary.

To invoke test run:

.. code-block:: console

    $ tox

Pre-Commit Hook - Ensuring / Enforcing Code Conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For ensuring to not push any errors that contradicts the Plone coding conventions please set a git pre-commit hook by adding one of the following commands to ``.git/hooks/pre-commit``:

.. code-block:: shell

    # full tests before a commit
    tox

    # or just code convention tests:
    tox -e isort,flake8

Cutting a release
^^^^^^^^^^^^^^^^^

To cut a release we use zest.releaser which could be installed via a separate virtualenv or as a shortcut for normal bugfix-releases run:

.. code-block:: console

    $ tox -e release

Support
-------

If you are having issues, please let us know.
