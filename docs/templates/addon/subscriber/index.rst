=========================
Subscriber sub-template
=========================

.. topic:: Description

    Adding a subscriber to an existing add-on package.


With this sub-template, you can add an event subscriber (handler) to a Plone add-on package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todo bobtemplates.plone:addon

then change into the created folder ``collective.todo`` and create your first View:

.. code-block:: shell

    mrbob bobtemplates.plone:subscriber

It will ask you for the subscriber handler file name and then creates this file in the subscribers folder. This file contains a handler method which you customize to your needs.


Example
=======

.. code-block:: shell

    $ cd collective.todo


Add a subscriber
----------------------------

.. code-block:: shell

    $ mrbob bobtemplates.plone:subscriber

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.



    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Subscriber handler file name (without extension) [obj_modified_do_something]: obj_mod_clear_cache

    >>> reading Plone version from bobtemplate.cfg

    rename example zcml file
    Should we run?:
    git add .
    git commit -m "Add subscriber: obj_mod_clear_cache"
    in: /home/maik/develop/src/collective.todo
    [y]/n:
    RUN: git add .
    RUN: git commit -m "Add subscriber: obj_mod_clear_cache"
    [master 53d7e16] "Add subscriber: obj_mod_clear_cache"
    5 files changed, 47 insertions(+)
    create mode 100644 src/collective/todo/subscribers/__init__.py
    create mode 100644 src/collective/todo/subscribers/configure.zcml
    create mode 100644 src/collective/todo/subscribers/obj_mod_clear_cache.py
    create mode 100644 src/collective/todo/tests/test_subscriber_obj_mod_clear_cache.py
