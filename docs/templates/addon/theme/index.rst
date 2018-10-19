==================
Theme sub-template
==================

.. topic:: Description

    Adding a theme to an existing add-on package.


With this sub-template, you can add a Plone theme to a Plone package. This theme template is useful to integrate existing themes or mockups from Designers into Plone. It doesn't come with any bacelonata resources nor does it make any assumptions how you build your static file like LESS, SCSS or JavaScript. You have to build your own setup for this. We do this because, many themes come with a different set of tools, so just use the tooling of the theme or build your own if there isn't any.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O plonetheme.blacksea bobtemplates.plone:addon

then change into the created folder ``plonetheme.blacksea`` and your theme:

.. code-block:: shell

    mrbob bobtemplates.plone:theme

It will ask you about the name of your theme and will generate the structure of your theme and also register it inside the Plone package.

The only thing you might want to add to your setup.py manually are the two following packages, which are to be added to the ``install_requires``:

- `collective.themesitesetup <https://pypi.python.org/pypi/collective.themesitesetup/>`_
- `collective.themefragments <https://pypi.python.org/pypi/collective.themefragments/>`_

These packages are optional but recommended to have support for configuration and additional PageTemplate thru theme packages. If you want to deploy your theme later as a ZIP-Files, be aware that these packages should be installed on the server as well.

Themes which are supporting these additional functionality are called ``Extended Themes``.

