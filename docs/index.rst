===================
bobtempalates.plone
===================

.. topic:: Description

    Overview of bobtemplates.plone features, compatibility and installation.

..  toctree::
    :maxdepth: 2

    templates/index
    git-support
    upgrade-packages
    develop

Introduction
============

``bobtemplates.plone`` provides a `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ template to generate packages for Plone projects.

To create a package like ``collective.myaddon``

.. code-block:: shell

    pip install bobtemplates.plone
    mrbob -O collective.myaddon bobtemplates.plone:addon

You can also create a package with nested name space

.. code-block:: shell

    mrbob -O collective.foo.myaddon bobtemplates.plone:addon

.. note::

    With the `plonecli <https://pypi.python.org/pypi/plonecli>`_, we have a nice commandline client for bobtemplates.plone. We highly recommend to use the plonecli, because it adds auto completion and some nice helpers to bobtemplate.plone.

Features
========

packages created with ``bobtemplates.plone`` use the current best-practices when creating an add-on and does all of boilerplate for you.

Provided templates
------------------

 - addon

  - behavior
  - content_type
  - portlet
  - theme
  - theme_barceloneta
  - view
  - viewlet
  - vocabulary

 - buildout
 - theme_package [deprecated] >> Please use the theme_barceloneta subtemplate!

.. note::

    For the full list of supported templates/subtemplates, you can use:
    ``plonecli -l``


Compatibility
=============

Add-on's created with ``bobtemplates.plone`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.
It should work on Linux, Mac and Windows.


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


This creates a mrbob-executable in your bin-directory.
Call it from the ``src``-directory of your Plone project like this.

.. code-block:: shell

    ../bin/mrbob -O collective.foo bobtemplates:addon


Installation in a Virtualenv
----------------------------

You can also install ``bobtemplates.plone`` in a Virtualenv.

.. code-block:: shell

    pip install bobtemplates.plone

With ``pip 6.0`` or newer ``mr.bob`` will automatically be installed as a dependency. If you still use a older version of pip you need install ``mr.bob`` before ``bobtemplates.plone``.

.. code-block:: shell

    pip install mr.bob

Now you can use it like this

.. code-block:: shell

    mrbob -O collective.foo bobtemplates:addon

See `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ documentation for further information.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

