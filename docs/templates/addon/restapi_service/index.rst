=============================
Rest-API-Service sub-template
=============================

.. topic:: Description

    Adding a restapi_service to an existing add-on package.


With this sub-template, you can add a restapi_service to a Plone package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todos bobtemplates.plone:addon

then change into the created folder ``collective.todos`` and create your restapi_service:

.. code-block:: shell

    mrbob bobtemplates.plone:restapi_service

It will ask you about the name of your Rest-API service class and name.

You will find the created restapi_service in the services folder inside the api folder.
