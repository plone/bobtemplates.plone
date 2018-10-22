======================
Theme Package template
======================

.. topic:: Description

    Creating a Plone package with a Barceloneta theme.


With this ``template``, you can create a full theme package at once.
This will create a Plone package with a Barceloneta theme including a full Grunt setup and a copy of all Barceloneta resources.

If you like it a bit more modular or you don't want to use the Barceloneta theme as a start, you might want to use the :doc:`theme  sub-template  </templates/addon/theme/index>` instead!

.. note::

    The theme_package template is deprecated, please use :doc:`theme_barceloneta  sub-template  </templates/addon/theme_barceloneta/index>` inside an existing add-on package.

.. code-block:: shell

    mrbob -O plonetheme.blacksea bobtemplates.plone:theme_package

then change into the created folder ``plonetheme.blacksea`` initialize it as followed:

.. code-block:: shell

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/buildout

After that you can start the Plone instance and activate your theme.
