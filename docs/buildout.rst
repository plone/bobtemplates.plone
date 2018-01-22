=============================
Create Plone buildout package
=============================

With this template you can create a basic Plone buildout, which often used as a project buildout. The project buildout then can contain all project related packages directly or as separate repositoris.

.. code-block:: sh

    mrbob bobtemplates.plone:buildout -O my_project

This will create a buildout folder for you.

.. code-block:: sh

    $ tree -L 2 my_project/
    my_project/
    ├── buildout.cfg
    ├── requirements.txt
    └── src

To initialize the buildout, change into the buildout folder and use the following commands:

.. code-block:: sh

    virtualenv .
    ./bin/pip install -r requirements.txt
    ./bin/buildout

