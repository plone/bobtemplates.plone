.. image:: https://github.com/plone/bobtemplates.plone/workflows/Plone%20package/badge.svg
    :target: https://github.com/plone/bobtemplates.plone/actions

.. image:: https://coveralls.io/repos/github/plone/bobtemplates.plone/badge.svg?branch=main
    :target: https://coveralls.io/github/plone/bobtemplates.plone?branch=main
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/bobtemplates.plone.svg?style=plastic
    :alt: Supported - Python Versions

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

.. note::

   With the `plonecli <https://pypi.python.org/pypi/plonecli>`_, we have a nice command line client for bobtemplates.plone.
   We highly recommend to use the plonecli, because it adds auto completion and some nice helpers to bobtemplates.plone.

Features
========

Package created with ``bobtemplates.plone`` use the current best-practices when creating an add-on. It also support's GIT by default, to keep track of changes one is doing with the bobtemplates.

Provided templates
------------------

- addon
- theme_package (Deprecated, use theme_barceloneta subtemplate)
- buildout (useful setup a development buildout or to test new pending Plone versions)


Provided subtemplates
---------------------

These templates are meant to be used inside a package which was created by the addon template.

- behavior
- content_type
- indexer
- portlet
- restapi_service
- subscriber
- theme
- theme_barceloneta
- upgrade_step
- view
- viewlet
- vocabulary


Compatibility
=============

Add-on's created with ``bobtemplates.plone`` are tested to work in **Plone >= 5.2** and **Python >= 3.7**.

If you need to create Plone packages for older versions of Plone and Python, please use bobtemplates.plone 5.x.
It should work on Linux, Mac and Windows.


Documentation
=============

Full documentation for end users and template developers can be found on `bobtemplatesplone.readthedocs.io <https://bobtemplatesplone.readthedocs.io>`_.

plonecli
--------

    For easy usage see: `plonecli <https://pypi.python.org/pypi/plonecli>`_


Installation
============

You can install bobtemplates.plone as every other normal Python package with `pip <https://pypi.python.org/pypi/pip>`_ user global or inside a virtualenv or better with `pipx <https://pypa.github.io/pipx/installation/>`_.

Installation with pip global for a user
---------------------------------------

.. code-block:: console

    pip install bobtemplates.plone --user


Installation with pipx
----------------------

pipx installs bobtemplates.plone and all dependencies in a global isolated virtualenv.

.. code-block:: console

    pipx install bobtemplates.plone


Installation with pip in a virtualenv
-------------------------------------

You can also install ``bobtemplates.plone`` with pip in a virtualenv.
If you don't have an active virtualenv, you can create one inside your project directory.

.. code-block:: bash

    python3 -m venv venv

Then either activate the virtualenv:

.. code-block:: bash

    source ./venv/bin/activate

or just use the binaries directly inside the bin folder as below:

.. code-block:: console

    ./venv/bin/pip install bobtemplates.plone


Usage
-----

As bobtemplates.plone is a template for mr.bob_, we use mrbob to run the templates.

If you are using pipx or have bobtemplates.plone globally installed, you can just use mrbob directly.

.. code-block:: console

    mrbob bobtemplates.plone:addon -O src/collective.foo

If you are using an unactivated virtualenv, you can use mrbob like this:

.. code-block:: console

    ./venv/bin/mrbob bobtemplates.plone:addon -O src/collective.foo

If you are using an activated virtualenv, you can use mrbob like this:

Activate your virtualenv:

.. code-block:: console

    source venv/bin/activate

.. code-block:: console

    mrbob bobtemplates.plone:addon -O src/collective.foo

This will create your Plone package inside the ``src`` directory.

See the documentation of mr.bob_ for further information.


Configuration
=============

You can set all `mr.bob configuration <http://mrbob.readthedocs.io/en/latest/userguide.html#configuration>`_ parameters in your ~/.mrbob file.

Here is an example:

.. code-block:: bash

    [mr.bob]
    verbose = False

    [variables]
    author.name = Maik Derstappen
    author.email = md@derico.de
    author.github.user = MrTango
    plone.version = 5.1.3-pending
    #package.git.init = y
    #package.git.autocommit = n
    #package.git.disabled = n

    [defaults]
    dexterity_type_global_allow = n
    dexterity_type_filter_content_types = y
    dexterity_type_activate_default_behaviors = n
    dexterity_type_supermodel = n


Contribute
==========

- Issue Tracker: https://github.com/plone/bobtemplates.plone/issues
- Source Code: https://github.com/plone/bobtemplates.plone
- Documentation: https://docs.plone.org/develop/addons/bobtemplates.plone/docs/ or https://bobtemplatesplone.readthedocs.io/en/latest/


Support
=======

If you are having issues, please let us know.
We have a Gitter channel here: `plone/bobtemplates.plone <https://gitter.im/plone/bobtemplates.plone>`_
