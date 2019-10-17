===============================
Upgrade existing Plone packages
===============================

bobtemplate.cfg
===============

To upgrade an existing Plone package, to work with the new sub-templates and also the plonecli. You simply need to add a bobtemplate.cfg with some content like this::

    [main]
    version = 5.2
    template = plone_addon
    python = python3.7

The version is used to make a difference in some templates, either for Plone 5 or Plone 4 packages. You can always create an addon package with the plonecli and copy over the bobtemplate.cfg in your old package.

other files
===========

You should have at leased a requirements.txt and a buildout.cfg file.
But it's recommended to add the following files from a generated addon package into your existing package:

- requirements.txt
- constraints.txt
- constraints_plone52.txt
- constraints_plone51.txt
- test_plone52.cfg
- test_plone51.cfg
- tox.ini

Folder structure
================

Since this package expects a specific folder structure, you should compare it to your existing structure and adjust it, where needed.

Upgrade steps
=============

The upgrade_step sub-template uses an upgrades folder to create upgrade steps in it. Therefor you should adjust existing upgrade step configuration to it.
You can have a look at `Products.EasyNewsletter <https://github.com/collective/Products.EasyNewsletter/tree/master/src/Products/EasyNewsletter>`_ where this was done.
