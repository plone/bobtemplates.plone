
.. image:: https://secure.travis-ci.org/plone/bobtemplates.plone.png?branch=master
    :target: http://travis-ci.org/plone/bobtemplates.plone

.. image:: https://coveralls.io/repos/github/plone/bobtemplates.plone/badge.svg?branch=master
    :target: https://coveralls.io/github/plone/bobtemplates.plone?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/bobtemplates.plone.svg
    :target: https://pypi.python.org/pypi/bobtemplates.plone/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/bobtemplates.plone.svg?style=plastic   :alt: Supported - Python Versions

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

    With the `plonecli <https://pypi.python.org/pypi/plonecli>`_, we have a nice commandline client for bobtemplates.plone. We highly recommend to use the plonecli, because it adds auto completion and some nice helpers to bobtemplate.plone.


Features
========

Package created with ``bobtemplates.plone`` use the current best-practices when creating an add-on. It also support's GIT by default, to keep track of changes one is doing with the bobtemplates.

Provided templates
------------------

- addon
- theme_package (Deprecated, use theme_barceloneta subtemplate)
- buildout


Provided subtemplates
---------------------

These templates are meant to be used inside a package which was created by the addon template.

- behavior
- content_type
- restapi_service
- theme
- theme_barceloneta
- view
- viewlet
- vocabulary

Compatibility
=============

Add-ons created with ``bobtemplates.plone`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.
It should work on Linux, Mac and Windows.


Documentation
=============

Full documentation for end users and template developers can be found in the "docs" folder.

    For easy usage see: `plonecli <https://pypi.python.org/pypi/plonecli>`_

It is also available online at http://docs.plone.org/develop/addons/bobtemplates.plone/docs/

Installation
============

You can install bobtemplates.plone as every other normal Python package with `pip <https://pypi.python.org/pypi/pip>`_ inside a `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ or better with `pipenv <https://pypi.python.org/pypi/pipenv>`_.


Installion with pipenv
----------------------

.. code-block:: console

    pipenv install bobtemplates.plone


Installation with pip in a virtualenv
-------------------------------------

You can also install ``bobtemplates.plone`` with pip in a virtualenv.
If you don't have an active virtualenv, you can create one inside your project directory.

.. code-block:: bash

    virtualenv .

Then either activate the virtualenv:

.. code-block:: bash

    source ./bin/activate

or just use the binaries directly inside the bin folder as below:

.. code-block:: console

    ./bin/pip install bobtemplates.plone


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


Usage
-----

As bobtemplates.plone is a template for mr.bob_, we use mrbob to run the templates.

If you are using `buildout <https://pypi.python.org/pypi/zc.buildout>`_  or an unactivated `virtualenv <https://pypi.python.org/pypi/virtualenv>`_, you can use mrbob like this:

.. code-block:: console

    ./bin/mrbob bobtemplates.plone:addon -O src/collective.foo

If you are using pipenv or an activated virtualenv, you can use mrbob like this:

Activate pipenv shell:

.. code-block:: console

    pipenv shell

or activate your virtualenv:

.. code-block:: console

    source bin/activate

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
