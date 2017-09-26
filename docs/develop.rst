=======================================
Developing bobtemplates.plone templates
=======================================

We can have standalone templates and subtemplates for bobtemplates.plone. By convention we will use a python module for every template and use some generic functions from the base module. All templates are living inside the bobtemplates/plone folder, in there own folder. All module files are placed inside the bobtemplates/plone folder and are referenced from hook commands in the ``.mrbob.ini`` file in the templates folders.

Standalone templates
=====================

Standalone templates are normal templates for mrbob which are meant to live standalone and are not depending on any other template. Examples are the ``buildout`` and ``addon`` templates. For details see the documentation of the mrbob package.

Subtemplates
============

Subtemplates are templates which are living inside an existing standalone template structure like the ``addon`` template. These templates extend the existing standalone template structure by new features like a ``theme`` or a ``content_type``. Subtemplates are searching first for the setup.py of the package and configure all needed parameters with this information.

Every subtemplate should define a prepare_renderer and a post_renderer hook method in there module.

.. code-block:: python

   from bobtemplates.plone.base import base_prepare_renderer


   def prepare_renderer(configurator):
       configurator = base_prepare_renderer(configurator)
       configurator.variables['template_id'] = 'content_type'


   def post_renderer(configurator):
       """
       """

As you can see, by convention we define a template_id here. We also call the base_prepare_renderer method from the base module first to setup some variables. If you need you can override or extend the variables, like we do in the ``content_type`` module with the ``target_folder``.

.. code-block:: python

   configurator.target_directory = configurator.variables['package_folder']

These prepare and post render methods are referenced in the ``.mrbob.ini`` file as follow:

.. code-block:: ini

   [template]
   pre_render = bobtemplates.plone.<YOURTEMPLATE_MODULE>:prepare_renderer
   post_render = bobtemplates.plone.<YOURTEMPLATE_MODULE>:post_renderer

The post_renderer method is a good place to update configuration files like we do in the ``theme`` and ``content_type`` subtemplates. You can also print some useful advice for the developer here.


Testing
=======

All templates and subtemplates should have tests for the structure they provide. These test will give the developers a good starting point. So that they only need to write test for there own code. Also these tests will be called on travis to make sure all by bobtemplates.plone created structures are working and tested. To run these test we run all templates in every combination and run the tests inside the created packages.

This could be for example the ``addon`` alone. Or for a package with Dexterity content types, first the ``addon`` template and then inside the created package the ``content_type`` subtemplate. The test are running after all templates for a case are applied.

By the time or writing this, we have the following cases (combinations), which we are testing:

- buildout
- addon
- addon + theme
- addon + content_type
- addon + theme + content_type
- theme_package
