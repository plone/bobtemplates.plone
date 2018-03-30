===================
Adding a vocabulary
===================



With this ``subtemplate``, you can add a dynamic `Vocabulary <https://docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/vocabularies.html#vocabularies>`_ to a Plone package.

First create a Plone Addon Package:

.. code-block:: sh

    mrbob -O collective.todos bobtemplates.plone:addon

then change into the created folder ``collective.todos`` and create your Vocabulary_:

.. code-block:: sh

    mrbob bobtemplates.plone:vocabulary

It will ask you about the name of your Vocabulary_ class.

You will find the created Vocabulary_ in the vocabularies folder. You need to change the concrete code to generate your Vocabulary_ terms. You will also find your Vocabulary_ in the Dexterity schema editor in your Browser. Your Vocabulary_ is registered in the configure.zcml, there you can find also the name of the Vocabulary_ under which you can get it in Python code.
