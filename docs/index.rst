===================
bobtempalates.plone
===================

.. topic:: Description

    Overview of bobtemplates.eea features, compatibility and installation.

..  toctree::
    :maxdepth: 2

    templates/index
    git-support
    upgrade-packages
    develop

Introduction
============

``bobtemplates.eea`` provides a `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ template to generate packages for Plone projects.

To create a package like ``collective.myaddon``

.. code-block:: shell

    pip install bobtemplates.eea
    mrbob -O collective.myaddon bobtemplates.eea:addon

You can also create a package with nested name space

.. code-block:: shell

    mrbob -O collective.foo.myaddon bobtemplates.eea:addon

.. note::

    With the `plonecli <https://pypi.python.org/pypi/plonecli>`_, we have a nice commandline client for bobtemplates.eea. We highly recommend to use the plonecli, because it adds auto completion and some nice helpers to bobtemplates.eea.

Features
========

packages created with ``bobtemplates.eea`` use the current best-practices when creating an add-on and does all of boilerplate for you.

Provided templates
------------------

 - addon

  - behavior
  - content_type
  - portlet
  - restapi_service
  - theme
  - theme_barceloneta
  - view
  - viewlet
  - vocabulary

 - buildout
 - theme_package [deprecated] >> Please use the theme_barceloneta sub-template!

.. note::

    For the full list of supported templates/subtemplates, you can use:
    ``plonecli -l``


Compatibility
=============

Add-on's created with ``bobtemplates.eea`` are tested to work in Plone 4.3.x and Plone 5.
They should also work with older versions but that was not tested.
It should work on Linux, Mac and Windows.


Installation
============

Installation global for a user (recommended)
--------------------------------------------

To have ``bobtemplates.eea`` and the `plonecli <https://pypi.python.org/pypi/plonecli>`_ always avilable, it's recommended to install it globally for your user.

.. code-block:: shell

    pip install plonecli --user

This will install the ``plonecli`` and ``bobtemplates.eea``. If you only want ``bobtemplates.eea``, you install only this package as follow:

.. code-block:: shell

    pip install bobtemplates.eea --user


Installation in a Virtualenv
----------------------------

You can also install ``bobtemplates.eea`` in a Virtualenv.

.. code-block:: shell

    pip install bobtemplates.eea

With ``pip 6.0`` or newer ``mr.bob`` will automatically be installed as a dependency. If you still use a older version of pip you need install ``mr.bob`` before ``bobtemplates.eea``.

.. code-block:: shell

    pip install mr.bob


Use plonecli and bobtemplates.eea
-----------------------------------

You can use the bobtemplates now with the ``plonecli``:

.. code-block:: shell

    plonecli create addon src/collective.foo
    cd src/collective.foo
    plonecli add content_type
    plonecli build test serve

.. code-block:: shell

    mrbob bobtemplates.eea:addon -O collective.foo
    cd src/collective.foo
    mrbob bobtemplates.eea:content_type
    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/buildout
    ./bin/test
    ./bin/instance fg

Changing the default Python and Plone versions
..............................................

By default you will build a virtualenv with Python2.7 and a buildout Plone 5.2. You can change this by customizing the buildout.cfg to extend one of the other test file, like test_plone43.cfg. Also you can change the requirements.txt to point to another constraints file like constraints_plone43.txt.

Additional information on plonecli and mrbob
--------------------------------------------

See `plonecli <https://pypi.python.org/pypi/plonecli>`_ and `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ documentation for further information.


Installing and using it in a buildout
-------------------------------------

::

    [buildout]
    parts += mrbob

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.eea


This creates a mrbob-executable in your bin-directory.
Call it from the ``src``-directory of your Plone project like this.

.. code-block:: shell

    ../bin/mrbob -O collective.foo bobtemplates:addon


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

