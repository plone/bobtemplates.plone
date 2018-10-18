====================================================================
Creating a Plone theme package based on Barceloneta inside a package
====================================================================

With this ``template``, you can add a Barceloneta based template to a Plone package. This will add a copy of Barceloneta theme including a full Grunt setup and a copy of all Barceloneta resources.

If you like it a bit more modular or you don't want add the Barceloneta Theme as a start, you might want to use the :doc:`theme subtemplate </theme>` instead!

.. code-block:: sh

    mrbob -O plonetheme.blacksea bobtemplates.plone:addon

then change into the created folder ``plonetheme.blacksea`` and add a new theme:

.. code-block:: sh

    mrbob bobtemplates.plone:theme


then initialize it as folowed:

.. code-block:: sh

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/buildout

After that you can start the Plone instance and activate your theme.

You will find more information about how to develop the new theme in the file DEVELOP_THEME.rst inside the addon folder.
