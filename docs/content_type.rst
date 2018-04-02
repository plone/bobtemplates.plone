=================================
Creating a Dexterity Content Type
=================================
`Title <http://link>`_
With this ``subtemplate``, you can add a `Dexterity <https://docs.plone.org/develop/plone/content/dexterity.html#dexterity>`_ Content Type to a Plone package.

First create a Plone Addon Package:

.. code-block:: sh

    mrbob -O collective.todos bobtemplates.plone:addon

then change into the created folder ``collective.todos`` and create your first Content Type:

.. code-block:: sh

    mrbob bobtemplates.plone:content_type

It will ask you about the name of your Content Type and will use this name also for classes, interfaces. You also have the choice of using the XML supermodel or the zope.schema to define the models. The default base class is Container, but you can choose also Item. By default the template will create a class for every content type, but you can decide to use the generic Dexterity classes if you don't need your own content type classes.
