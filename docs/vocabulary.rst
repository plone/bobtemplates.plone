===================
Adding a vocabulary
===================

With this ``subtemplate``, you can add a dynamic vocabulary to a Plone package.

First create a Plone Addon Package:

.. code-block:: sh

    mrbob -O collective.todos bobtemplates.plone:addon

then change into the created folder ``collective.todos`` and create your first Content Type:

.. code-block:: sh

    mrbob bobtemplates.plone:vocabulary

It will ask you about the name of your vocabulary class.

You will find the created vocabulary in the vocabularies folder. You need to change the concrete code to generate your vocabulary terms. You will also find your vocabulary in the Dexterity schema editor in your Browser. Your vocabulary is registered in the configure.zcml, there you can find also the name of the vocabulary under which you can get it in Python code.
