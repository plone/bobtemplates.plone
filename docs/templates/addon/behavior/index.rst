=====================
Behavior sub-template
=====================

.. topic:: Description

    Adding a custom Behavior to an existing add-on package.


With this ``sub-template``, you can add a `Behavior <https://docs.plone.org/develop/plone/content/behaviors.html#behaviors>`_ to a Plone package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todos bobtemplates.plone:addon

then change into the created folder ``collective.todos`` and create your Behavior_:

.. code-block:: shell

    mrbob bobtemplates.plone:behavior

It will ask you about the name of your Behavior_ class.

You will find the created behavior in the behaviors folder. You need to add the concrete code to your Behavior_.
