===============================
Upgrade existing Plone packages
===============================

To upgrade an existing Plone package, to work with the new sub-templates and also the plonecli. You simply need to add a bobtemplate.cfg with some content like this::

    [main]
    version = 5.1
    template = plone_addon


The version is used to make a difference in some templates, either for Plone 5 or Plone 4 packages. You can always create an addon package with the plonecli and copy over the bobtemplate.cfg in your old package.
