=====
addon
=====

.. topic:: Description

    Creating an addon package and extending it with subtemplates.

..  toctree::
    :maxdepth: 2
    :glob:

    */index

With this template you can create a basic Plone package.

.. code-block:: sh

    mrbob -O collective.todos bobtemplates.plone:addon

This will create a Python package for you, which you can extend manually or by using other subtemplates like ``theme`` or ``content_type`` from bobtemplates.plone.

