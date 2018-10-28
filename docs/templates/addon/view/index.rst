=========================
View sub-template
=========================

.. topic:: Description

    Adding a View to an existing add-on package.


With this sub-template, you can add a `View <https://docs.plone.org/develop/plone/views/browserviews.html>`_ to a Plone add-on package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todo bobtemplates.plone:addon

then change into the created folder ``collective.todo`` and create your first View:

.. code-block:: shell

    mrbob bobtemplates.plone:view

It will ask if you need Python class and template file, you can have both or at least one to have a working view. Based on the input it will ask about class name, template name or both. By default it will suggest you to use class name as view name (the part of url) but you can also change it. You can see your newly created view by using the url that you used for view name on ``IFolderish`` interface.


Example
=======

.. code-block:: shell

    $ cd collective.todo


Add a View
----------------------------

.. code-block:: shell

    $ mrbob bobtemplates.plone:view

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.



    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Should the view have a Python class? [y]: y

    --> Python class name [MyView]: DemoView

    --> View name (part of the URL) [demo-view]: demo-view

    --> Should the View have a template file? [y]: 

    --> Template name (without extension) [demo_view]: demo

    >>> reading Plone version from bobtemplate.cfg

    Should we run?:
    git add .
    git commit -m "Add view: demo-view"
    in: /Users/akshay/plone/collective.todo
    [y]/n: y
    RUN: git add .
    RUN: git commit -m "Add view: demo-view"
    [master 64d8a8b] "Add view: demo-view"
    4 files changed, 93 insertions(+)
    create mode 100644 src/collective/todo/tests/test_view_demo_view.py
    create mode 100644 src/collective/todo/views/demo.pt
    create mode 100644 src/collective/todo/views/demo_view.py

    Generated file structure at /Users/akshay/plone/collective.todo
