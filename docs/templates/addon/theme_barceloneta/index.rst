==============================
Theme Barceloneta sub-template
==============================

.. topic:: Description

    Adding a barceloneta theme to an existing add-on package.


With this sub-template, you can add a Plone theme to a Plone package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O plonetheme.blacksea bobtemplates.plone:addon

then change into the created folder ``plonetheme.blacksea`` and your theme:

.. code-block:: shell

    mrbob bobtemplates.plone:theme_barceloneta

It will ask you about the name of your theme and will generate the structure of your theme and also register it inside the Plone package.

The only thing you might want to add to your setup.py manually are the two following packages, which are to be added to the ``install_requires``:

- `collective.themesitesetup <https://pypi.python.org/pypi/collective.themesitesetup/>`_
- `collective.themefragments <https://pypi.python.org/pypi/collective.themefragments/>`_

These packages are optional but recommended to have support for configuration and additional PageTemplate thru theme packages. If you want to deploy your theme later as a ZIP-Files, be aware that these packages should be installed on the server as well.

Themes which are supporting these additional functionality are called ``Extended Themes``.

