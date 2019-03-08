=======================================
Developing bobtemplates.plone templates
=======================================

Setup dev environment
=====================

In the package folder create a virtualenv and install the package:

.. code-block:: shell

   virtualenv --clear .
   ./bin/python setup.py develop


Intro
=====

We can have standalone templates and sub-templates for bobtemplates.plone.
By convention we will have a python module and a template folder for every template and use some generic functions from the base module.

All templates are living inside the ``bobtemplates/plone`` folder, in their own template folder.
All module files are placed inside the ``bobtemplates/plone`` folder and are referenced from hook commands in the ``.mrbob.ini`` file in the template folders.
They get called by different ``mrbob hooks``, like ``pre_render``, ``post_render`` or ``pre_question hook`` and so on.


Standalone templates
====================

Standalone templates are normal templates for mrbob, which are meant to live standalone and are not depending on any other template.

Examples are the ``buildout`` and ``addon`` templates. For details see the documentation of the mrbob package.


Sub-templates
=============

Sub-templates are templates which are living inside an existing package created by a standalone template like the ``addon`` template.
These templates extend the existing standalone template structure by new features like a ``theme`` or a ``content_type``.

Sub-templates are searching first for the ``setup.py`` and a ``bobtemplate.cfg`` file inside the package and configure all needed parameters with this information.
See also :doc:`upgrade-packages` to see how to upgrade an existing package to be compatible with sub-templates.
Every sub-template should define a ``pre_renderer`` and a ``post_renderer`` hook in their ``.mrbob.ini`` which points to a method in their sub-templates module.

.. code-block:: ini

   [template]
   pre_render = bobtemplates.plone.<YOURTEMPLATE_MODULE>:pre_renderer
   post_render = bobtemplates.plone.<YOURTEMPLATE_MODULE>:post_renderer


.. code-block:: python

   from bobtemplates.plone.base import base_prepare_renderer


   def pre_renderer(configurator):
       configurator = base_prepare_renderer(configurator)
       configurator.variables['template_id'] = 'content_type'


   def post_renderer(configurator):
       """
       """


As you can see, by convention we define a template_id here. We also call the base_prepare_renderer method from the base module first to setup some generic variables. The ``pre_renderer`` hook is a good place to set template specific variables. If you need you can override or extend the variables, like we do in the ``content_type`` module with the ``target_folder``.

.. code-block:: python

   configurator.target_directory = configurator.variables['package_folder']


The ``post_renderer`` method is a good place to update configuration files, like we do for example in the ``theme`` and ``content_type`` sub-templates.

You can also print some useful advice for the developer here, as we do in the ``vocabulary`` sub-template for example.


Template Registration
=====================

Even though you can use bobtemplates without registration, you should register the template to allow plonecli and future mrbob versions to query for it.
The registration is done by adding a Python entry point into the ``setup.py`` of ``bobtemplates.plone`` and by adding a short method to the ``bobregistry.py`` file.
You can of course create your own custom package, analog to bobtemplates.plone and register your templates plonecli the same way.
This could be used for example for your agency or client specific code structures. If you need help by creating such custom bobtemplates and plonecli integration's, give us a sign on Gitter: https://gitter.im/plone/plonecli.

Let's look first on the entry point:

.. code-block:: python

    entry_points={
        'mrbob_templates': [
            'plone_addon = bobtemplates.plone.bobregistry:plone_addon',
            'plone_content_type = bobtemplates.plone.bobregistry:plone_content_type',
            'plone_vocabulary = bobtemplates.plone.bobregistry:plone_vocabulary',
        ],

This registers every template globally for mrbob and tools like plonecli. The first part is the global template name and the second part points to a method in the bobregistry module. This method gives back some details for the template.

.. code-block:: python

    def plone_vocabulary():
        reg = RegEntry()
        reg.template = 'bobtemplates.plone:vocabulary'
        reg.plonecli_alias = 'vocabulary'
        reg.depend_on = 'plone_addon'
        return reg

The method defines the following things:

- ``template``: the mrbob template to use
- ``plonecli_alias``: a short name alias which will be used by plonecli
- ``depend_on``: an optional global parent template

We use here globally unique template names which have the ``plone_`` prefix.
That is because other ``bobtemplate`` packages might register templates too and we want to avoid name clashes.

Testing
=======

All templates and sub-templates should have tests for the structure they provide.

These tests will give developers a good starting point to write tests for their own code.
Also these tests will be called by Tox and on Travis to make sure that all the structures created by ``bobtemplates.plone`` are working and tested.

We run tests for both all the templates with every combination and inside the generated packages.

For example tests could be run only on ``addon``.
Alternately, for a package with Dexterity content types, tests could be run first for the ``add-on`` template, then inside the package created by the ``content_type`` sub-template.

The tests are running after all templates for a case are applied.

To run all tests locally, just run ``tox`` without any parameter.
You can also run individual tests for a specific environment. To get a list of all environments run ``tox -l``.

.. code-block:: shell

    $ tox -l
    py37-lint
    py27-lint
    docs
    py27-packagetests
    py37-packagetests
    py27-skeletontests-Plone43-template-addon
    py27-skeletontests-Plone51-template-addon
    py27-skeletontests-Plone52-template-addon
    py37-skeletontests-Plone52-template-addon
    py27-skeletontests-Plone43-template-addon_content_type
    py27-skeletontests-Plone51-template-addon_content_type
    py27-skeletontests-Plone52-template-addon_content_type
    py37-skeletontests-Plone52-template-addon_content_type
    py27-skeletontests-Plone43-template-addon_view
    py27-skeletontests-Plone51-template-addon_view
    py27-skeletontests-Plone52-template-addon_view
    py37-skeletontests-Plone52-template-addon_view
    py27-skeletontests-Plone43-template-addon_viewlet
    py27-skeletontests-Plone51-template-addon_viewlet
    py27-skeletontests-Plone52-template-addon_viewlet
    py37-skeletontests-Plone52-template-addon_viewlet
    py27-skeletontests-Plone43-template-addon_portlet
    py27-skeletontests-Plone51-template-addon_portlet
    py27-skeletontests-Plone52-template-addon_portlet
    py37-skeletontests-Plone52-template-addon_portlet
    py27-skeletontests-Plone43-template-addon_theme
    py27-skeletontests-Plone51-template-addon_theme
    py27-skeletontests-Plone52-template-addon_theme
    py37-skeletontests-Plone52-template-addon_theme
    py27-skeletontests-Plone51-template-addon_theme_barceoneta
    py27-skeletontests-Plone52-template-addon_theme_barceoneta
    py37-skeletontests-Plone52-template-addon_theme_barceoneta
    py27-skeletontests-Plone43-template-addon_vocabulary
    py27-skeletontests-Plone51-template-addon_vocabulary
    py27-skeletontests-Plone52-template-addon_vocabulary
    py37-skeletontests-Plone52-template-addon_vocabulary
    py27-skeletontests-Plone43-template-addon_behavior
    py27-skeletontests-Plone51-template-addon_behavior
    py27-skeletontests-Plone52-template-addon_behavior
    py37-skeletontests-Plone52-template-addon_behavior
    py27-skeletontests-Plone43-template-addon_restapi_service
    py27-skeletontests-Plone51-template-addon_restapi_service
    py27-skeletontests-Plone52-template-addon_restapi_service
    py37-skeletontests-Plone52-template-addon_restapi_service
    py27-skeletontests-Plone43-template-theme_package
    py27-skeletontests-Plone51-template-theme_package
    coverage-report

You can run just one of them:

.. code-block:: sh

   tox -e py27-skeletontests-Plone52-template-addon

or call all of the same template but for different Plone versions:

.. code-block:: shell

   tox -e py27-skeletontests-Plone43-template-addon_content_type,py27-skeletontests-Plone51-template-add-on_content_type,py27-skeletontests-Plone52-template-add-on_content_type

.. note::

   There is no empty space between the list elements!

Running a specific test
-----------------------

The actual tests are written with the pytest module, therefor you can always run them with pytest directly.

To run a specific pytest with Tox, you can pass additional arguments to pytest, buy putting them after the ``--`` parameter.

.. code-block:: shell

    $ tox -e py36-packagetests -- -k test_set_global_vars

Increase verbosity of Tox/Pytest
................................

.. code-block:: shell

    tox -e py36-packagetests -vv -- -s

Package tests
.............

Package tests are for testing the code of bobtemplates.plone it self. These code is used to generate and update the structures of the generated packages.

You can find these test in the ``package-test`` folder.
This is a good place to test everything related to the generation process.

Skeleton tests
..............

Skeleton tests are for testing, that the generated packages are actually work. We generate the packages, with different combinations of sub-templates, build and run the tests inside.

The tests are defined in the directory ``skeleton-tests`` and are called by ``tox`` as defined in ``tox.ini``.

If you add new test cases (files), make sure that they are in the ``tox.ini`` and also included int the Travis matrix, see below!

Skeleton tests it self are using pytest too, but the tests inside the generated packages are Zope tests running by zc.testrunner.
Starting from version 4.x, packages generated by bobtemplates.plone are containing also a tox setup by them self. This allows you to easily test your package against multiple Python and Plone versions.

Generating Travis matrix from tox.ini
=====================================

.. code-block:: shell

    $ python tox2travis.py
    matrix:
        include:
            - env: TOXENV=py37-lint
            python: "3.7"
            - env: TOXENV=py27-lint
            - env: TOXENV=docs
            - env: TOXENV=py27-packagetests
            - env: TOXENV=py37-packagetests
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon
            - env: TOXENV=py27-skeletontests-Plone51-template-addon
            - env: TOXENV=py27-skeletontests-Plone52-template-addon
            - env: TOXENV=py37-skeletontests-Plone52-template-addon
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_content_type
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_content_type
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_content_type
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_content_type
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_view
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_view
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_view
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_view
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_viewlet
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_viewlet
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_viewlet
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_viewlet
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_portlet
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_portlet
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_portlet
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_portlet
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_theme
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_theme
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_theme
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_theme
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_theme_barceoneta
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_theme_barceoneta
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_theme_barceoneta
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_vocabulary
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_vocabulary
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_vocabulary
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_vocabulary
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_behavior
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_behavior
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_behavior
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_behavior
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-addon_restapi_service
            - env: TOXENV=py27-skeletontests-Plone51-template-addon_restapi_service
            - env: TOXENV=py27-skeletontests-Plone52-template-addon_restapi_service
            - env: TOXENV=py37-skeletontests-Plone52-template-addon_restapi_service
            python: "3.7"
            - env: TOXENV=py27-skeletontests-Plone43-template-theme_package
            - env: TOXENV=py27-skeletontests-Plone51-template-theme_package
            - env: TOXENV=coverage-report


replace the current matrix in ``.travis.yml`` with the result.
