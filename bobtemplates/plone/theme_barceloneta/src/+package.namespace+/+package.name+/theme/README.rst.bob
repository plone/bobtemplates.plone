=================
Theme Development
=================


Tooling
=======


Install dependencies
--------------------

Run `npm install` to add dependencies from package.json::

.. code-block:: shell

    $ npm install


Compile resources
-----------------

Run `npm run build` to add dependencies from package.json::

.. code-block:: shell

    $ npm run build

This will compile your `scss/theme.scss` into `css/theme.css`. A minified
version () will be created as well. Check out the scripts section from
`package.json` so see what happens exactly.


Watch for changes
-----------------

Run `npm run watch` to automatically compile when a file has been changed::

.. code-block:: shell

    $ npm run watch

With `npm run watch` you start the build process automatically when you save a file.


Configuring Plone within the theme package
==========================================

To configure Plone when this package is installed, you can use GenericSetup profiles in profiles/default.
To revert the settings when the package is being uninstalled, place the default Plone configurations inside the profiles/uninstall folder.


Providing new template or override existing once
================================================

Providing new templates
-----------------------

To add new views with your package, you can use plonecli.

.. code-block:: shell

    plonecli add view

Depending how you answered the questions, you will now have a new view, which can have a Python file for the logic and a template for the presentation.


Overriding existing templates
-----------------------------

To override a template, you place the template into the browser/overrides folder.

The name of the template has to be the dotted namespace + templatename.

.. code-block:: shell

    browser/overrides/plone.app.layout.viewlets.logo.pt

More info here:
https://pypi.org/project/z3c.jbot/



Providing new templates and Python Scripts, alternative solutions
=================================================================

- `collective.themefragments <https://pypi.python.org/pypi/collective.themefragments/>`_
- `plone.app.themingplugins <https://pypi.python.org/pypi/plone.app.themingplugins/>`_
- `collective.themesitesetup <https://pypi.python.org/pypi/collective.themesitesetup/>`_
