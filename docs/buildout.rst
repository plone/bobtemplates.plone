=============================
Create Plone Buildout Package
=============================

With this template you can create a basic Plone buildout, which often used as a project buildout. The project buildout then can contain all project related packages directly or as separate repositories.

.. code-block:: shell

    mrbob bobtemplates.plone:buildout -O my_project

This will ask you for a Plone version and will create a buildout folder for you. The buildout configuration is using the buildout.plonetest configurations provided by the Plone community for developing and testing Plone. For more information about the buildout.plonetest configurations see here: https://github.com/collective/buildout.plonetest

.. code-block:: shell

    $ tree -L 2 my_project/
    my_project/
    ├── bobtemplate.cfg
    ├── buildout.cfg
    ├── requirements.txt
    └── src

To initialize the buildout, change into the buildout folder and use the following commands:

.. code-block:: shell

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/buildout
