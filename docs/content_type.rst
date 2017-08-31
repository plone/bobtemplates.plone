=================================
Creating a Dexterity Content Type
=================================

With this ``subtemplate``, you can add a Dexterity Content Type to a Plone package.

First create a Plone Addon Package:

.. code-block:: sh

    mrbob -O collective.todos bobtemplates.plone:plone_addon

then change into the created folder ``collective.todos`` and create your first Content Type:

.. code-block:: sh

    mrbob bobtemplates.plone:content_type

It will ask you about the name of your Content Type and will use this name also for classes, interfaces.
