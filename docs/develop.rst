=======================================
Developing bobtemplates.plone templates
=======================================

Setup dev environment
=====================

In the package folder create a virtualenv and install the package:

.. code-block:: console

   virtualenv --clear .
   ./bin/python setup.py develop

Intro
=====

We can have standalone templates and subtemplates for bobtemplates.plone.
By convention we will use a python module for every template and use some generic functions from the base module.

All templates are living inside the bobtemplates/plone folder, in there own folder.
All module files are placed inside the bobtemplates/plone folder and are referenced from hook commands in the ``.mrbob.ini`` file in the templates folders.

Standalone templates
=====================

Standalone templates are normal templates for mrbob which are meant to live standalone and are not depending on any other template.

Examples are the ``buildout`` and ``addon`` templates. For details see the documentation of the mrbob package.

Subtemplates
============

Subtemplates are templates which are living inside an existing standalone template structure like the ``addon`` template.
These templates extend the existing standalone template structure by new features like a ``theme`` or a ``content_type``.

Subtemplates are searching first for the setup.py of the package and configure all needed parameters with this information.

Every subtemplate should define a prepare_renderer and a post_renderer hook method in their module.

.. code-block:: python

   from bobtemplates.plone.base import base_prepare_renderer


   def prepare_renderer(configurator):
       configurator = base_prepare_renderer(configurator)
       configurator.variables['template_id'] = 'content_type'


   def post_renderer(configurator):
       """
       """

As you can see, by convention we define a template_id here. We also call the base_prepare_renderer method from the base module first to setup some variables.
If you need you can override or extend the variables, like we do in the ``content_type`` module with the ``target_folder``.

.. code-block:: python

   configurator.target_directory = configurator.variables['package_folder']

These prepare and post render methods are referenced in the ``.mrbob.ini`` file as follow:

.. code-block:: ini

   [template]
   pre_render = bobtemplates.plone.<YOURTEMPLATE_MODULE>:prepare_renderer
   post_render = bobtemplates.plone.<YOURTEMPLATE_MODULE>:post_renderer

The post_renderer method is a good place to update configuration files like we do in the ``theme`` and ``content_type`` subtemplates.

You can also print some useful advice for the developer here.


Testing
=======

All templates and subtemplates should have tests for the structure they provide.

These test will give the developers a good starting point. So that they only need to write test for there own code.
Also these tests will be called by tox and on travis to make sure all by bobtemplates.plone created structures are working and tested.

To run these test we run all templates in every combination and run the tests inside the created packages.

This could be for example the ``addon`` alone. Or for a package with Dexterity content types,
first the ``addon`` template and then inside the created package the ``content_type`` subtemplate.

The tests are running after all templates for a case are applied.

To run all tests locally, just run ``tox`` without any parameter.
You can also run individual tests for a specific environment. To get a list of all environments run ``tox -l``.

.. code-block:: console

   tox -l
   py27-packagetests
   py34-packagetests
   py35-packagetests
   py36-packagetests
   pypy-packagetests
   py27-skeletontests-Plone-4.3-template-addon
   py27-skeletontests-Plone-5.0-template-addon
   py27-skeletontests-Plone-5.1-template-addon
   py27-skeletontests-Plone-4.3-template-addon_content_type
   py27-skeletontests-Plone-5.0-template-addon_content_type
   py27-skeletontests-Plone-5.1-template-addon_content_type
   py27-skeletontests-Plone-4.3-template-addon_theme
   py27-skeletontests-Plone-5.0-template-addon_theme
   py27-skeletontests-Plone-5.1-template-addon_theme
   py27-skeletontests-Plone-4.3-template-addon_vocabulary
   py27-skeletontests-Plone-5.0-template-addon_vocabulary
   py27-skeletontests-Plone-5.1-template-addon_vocabulary
   py27-skeletontests-Plone-4.3-template-theme_package
   py27-skeletontests-Plone-5.0-template-theme_package
   py27-skeletontests-Plone-5.1-template-theme_package
   lint-py27
   lint-py36
   docs
   coverage-report

You can run just one of them:

.. code-block:: console

   tox -e py27-skeletontests-Plone-5.1-template-addon

or call all of the same template but for different Plone versions:

.. code-block:: console

   tox -e py27-skeletontests-Plone-4.3-template-addon_content_type,py27-skeletontests-Plone-5.0-template-addon_content_type,py27-skeletontests-Plone-5.1-template-addon_content_type

.. note::

   There is no empty space between the list elements!

By the time or writing this, we have the following test cases (combinations), which we are testing:

- addon
- addon_content_type
- addon_theme
- addon_vocabulary
- theme_package

The test are defined in the directory ``skeleton-tests`` and are called by ``tox`` as defined in tox.ini.

If you add new test cases (files), make sure that they are in the tox.ini and also called by travis!
