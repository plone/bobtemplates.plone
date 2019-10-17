=========================
Indexer sub-template
=========================

.. topic:: Description

    Adding an indexer to an existing add-on package.


With this sub-template, you can add an indexer to a Plone add-on package, to define what and how an index get's filled.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todo bobtemplates.plone:addon

then change into the created folder ``collective.todo`` and create your first View:

.. code-block:: shell

    mrbob bobtemplates.plone:indexer

It will ask you for the indexer name and then creates a zcml config and a python file in the indexers folder for it. The Pyhon file contains a indexer method which you customize to your needs.


Example
=======

.. code-block:: shell

    $ cd collective.todo


Add a indexer
-------------

.. code-block:: shell

    $ mrbob bobtemplates.plone:indexer

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.

    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Indexer name [my_custom_index]: funky_title

    >>> reading Plone version from bobtemplate.cfg

    <include package=".indexers" />
    already in /home/maik/develop/src/collective.todo/src/collective/todo/configure.zcml, skip adding!
    Should we run?:
    git add .
    git commit -m "Add indexer: funky_title"
    in: /home/maik/develop/src/collective.todo
    [y]/n:
    RUN: git add .
    RUN: git commit -m "Add indexer: funky_title"
    [master 2f4e8f9] "Add indexer: funky_title"
    4 files changed, 53 insertions(+)
    create mode 100644 src/collective/todo/indexers/funky_title.py
    create mode 100644 src/collective/todo/indexers/funky_title.zcml
    create mode 100644 src/collective/todo/tests/test_indexer_funky_title.py
