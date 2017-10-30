
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

.. image:: https://badges.gitter.im/plone/bobtemplates.plone.svg
    :target: https://gitter.im/plone/bobtemplates.plone?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter channel

==================
bobtemplates.plone
==================

``bobtemplates.plone`` provides `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ templates to generate packages for Plone projects.

    **Note:** bobtemplates.plone supports `plonecli <https://pypi.python.org/pypi/plonecli>`_, which is the recommended way of creating Plone packages.


Features
========

Package created with ``bobtemplates.plone`` use the current best-practices when creating an add-on.

Provided templates
------------------

- addon
- theme_package
- buildout


Provided subtemplates
---------------------

These templates are meant to be used inside a package which was created by the addon template.

- theme
- content_type
- vocabulary


Compatibility
=============

Add-ons created with ``bobtemplates.plone`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.
It should work on Linux, Mac and Windows.


Documentation
=============

Full documentation for end users and developers can be found in the "docs" folder.

    For easy usage see: `plonecli <https://pypi.python.org/pypi/plonecli>`_

It is also available online at http://docs.plone.org/develop/addons/bobtemplates.plone/bobtemplates.plone/docs/

Installation
============

Use in a buildout
-----------------

.. code-block:: ini

    [buildout]
    parts += mrbob

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.plone


This creates a mrbob-executable in your bin-directory.
Call it from the ``src``-directory of your Plone project like this.

.. code-block:: console

    ../bin/mrbob bobtemplates.plone:addon -O collective.foo


Installation in a virtualenv
----------------------------

You can also install ``bobtemplates.plone`` in a virtualenv.

.. code-block:: console

    pip install bobtemplates.plone

With ``pip 6.0`` or newer ``mr.bob`` will automatically be installed as a dependency.
If you still use a older version of pip you need install ``mr.bob`` before ``bobtemplates.plone``.

.. code-block:: console

    pip install mr.bob

Now you can use it like this

.. code-block:: console

    mrbob bobtemplates.plone:addon -O collective.foo



See `the documentation of mr.bob <http://mrbob.readthedocs.org/en/latest/>`_  for further information.


Contribute
==========

- Issue Tracker: https://github.com/plone/bobtemplates.plone/issues
- Source Code: https://github.com/plone/bobtemplates.plone
- Documentation: http://docs.plone.org/develop/addons/bobtemplates.plone/bobtemplates.plone/docs/


Support
=======

If you are having issues, please let us know.
We have a Gitter channel here: `plone/bobtemplates.plone <https://gitter.im/plone/bobtemplates.plone>`_
