==============================
Creating a Plone theme package
==============================

With this ``template``, you can create a full theme package at once.
This will create a Plone package with a Barceloneta theme including a full Grunt setup and a copy of all Barceloneta resources.

If you like it a bit more modular or you don't want to use the Barceloneta Theme as a start, you meight want to use the :doc:`theme subtemplate </theme>` instead!

.. code-block:: sh

    mrbob -O plonetheme.blacksea bobtemplates.plone:theme_package

then change into the created folder ``collective.blacksea`` initialize it as folowed:

.. code-block:: sh

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/buildout

After that you can start the Plone instance and activate your theme.
