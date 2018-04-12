===============================
Upgrade existing Plone packages
===============================

bobtemplate.cfg
===============

To upgrade an existing Plone package, to work with the new sub-templates and also the plonecli. You simply need to add a bobtemplate.cfg with some content like this::

    [main]
    version = 5.1
    template = plone_addon

The version is used to make a difference in some templates, either for Plone 5 or Plone 4 packages. You can always create an addon package with the plonecli and copy over the bobtemplate.cfg in your old package.

requiremens.txt
===============

In case you don't have a ``requirements.txt`` already in your package repository, you should also add this::

    setuptools==38.2.4
    zc.buildout==2.10.0
