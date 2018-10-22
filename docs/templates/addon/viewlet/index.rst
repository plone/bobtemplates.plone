=========================
Viewlet sub-template
=========================

.. topic:: Description

    Adding a Viewlet to an existing add-on package.


With this sub-template, you can add a `Viewlet <https://docs.plone.org/develop/plone/views/viewlets.html>`_ to a Plone add-on package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todo bobtemplates.plone:addon

then change into the created folder ``collective.todo`` and create your first Viewlet:

.. code-block:: shell

    mrbob bobtemplates.plone:viewlet

It will ask if you need Python class and template file, you can have both or at least one to have a working viewlet. Based on the input it will ask about class name, template name or both. By default it will suggest you to use class name as viewlet name but you can also change it. This will create a viewlet registered to ``IAboveContentTitle`` viewlet manager and on ``IDocument`` interface.


Example
=======

.. code-block:: shell

    $ cd collective.todo


Add a Viewlet
----------------------------

.. code-block::shell
    
    $ mrbob bobtemplates.plone:viewlet

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.



    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Name of the Viewlet's Python class? [MyViewlet]: DemoViewlet

    --> Viewlet name [demo-viewlet]: 

    --> Should the viewlet have a template file? [y]: 

    --> Template name (without extension) [demo_viewlet]: 

    >>> reading Plone version from bobtemplate.cfg

    Should we run?:
    git add .
    git commit -m "Add viewlet: demo-viewlet"
    in: /Users/akshay/plone/collective.todo
    [y]/n: y
    RUN: git add .
    RUN: git commit -m "Add viewlet: demo-viewlet"
    [master 280b991] "Add viewlet: demo-viewlet"
    6 files changed, 103 insertions(+)
    create mode 100644 src/collective/todo/tests/test_viewlet_demo_viewlet.py
    create mode 100644 src/collective/todo/viewlets/__init__.py
    create mode 100644 src/collective/todo/viewlets/configure.zcml
    create mode 100644 src/collective/todo/viewlets/demo_viewlet.pt
    create mode 100644 src/collective/todo/viewlets/demo_viewlet.py

    Generated file structure at /Users/akshay/plone/collective.todo
