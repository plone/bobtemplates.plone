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


Upgrade notes
=============

Starting with version `6.3.x` we provide the latest `@plone/plonetheme-barceloneta-base==3.1.x` which
depends on Bootstrap 5.3 and adds the new "color mode" feature.

If you have generated a `theme_barceloneta` with version 6.2.x (Bootstrap 5.2.x) you can
easily update your theme to Bootstrap 5.3 with the following steps:

  1. pin `"@plone/plonetheme-barceloneta-base": "~3.1.0"` in you `package.json`
  2. install cleanly with `rm -rf node_modules package-lock.json && npm install` in your theme folder
  3. Fix your theme imports by adding the following lines to your `theme/styles/theme.scss`:
     `adding Bootstrap 5.3 color mode imports <https://github.com/plone/bobtemplates.plone/pull/550/commits/e61c34439582eac2b52fab15327c849a69e6da05?diff=unified&w=1>`_
  4. compile your css with `npm run build`
