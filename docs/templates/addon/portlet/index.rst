=========================
Portlet sub-template
=========================

.. topic:: Description

    Adding a Portlet to an existing add-on package.


With this sub-template, you can add a `Portlet <https://docs.plone.org/develop/plone/functionality/portlets.html>`_ to a Plone add-on package.

First create a Plone add-on package:

.. code-block:: shell

    mrbob -O collective.todo bobtemplates.plone:addon

then change into the created folder ``collective.todo`` and create your first Portlet:

.. code-block:: shell

    mrbob bobtemplates.plone:portlet

Portlets are used for wide variety of tasks in Plone and you can read about it in `Portlets reference manual <https://docs.plone.org/4/en/old-reference-manuals/portlets/index.html>`_ for in-depth information. It will just ask for the name of the portlet and the same name is used to create file structures and as well as the portlet name. This will create a basic portlet which ask for city name and country and it will fetch weather data of that city using Yahoo Weather API.


Example
=======

.. code-block:: shell

    $ cd collective.todo


Add a Portlet
----------------------------

.. code-block:: shell

    $ mrbob bobtemplates.plone:portlet

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.



    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Portlet name to display for the portlet [Weather]: My Weather Portlet

    >>> reading Plone version from bobtemplate.cfg

    Should we run?:
    git add .
    git commit -m "Add portlet: My Weather Portlet"
    in: /Users/akshay/plone/collective.todo
    [y]/n: 
    RUN: git add .
    RUN: git commit -m "Add portlet: My Weather Portlet"
    [master ea9d848] "Add portlet: My Weather Portlet"
    5 files changed, 177 insertions(+)
    create mode 100644 src/collective/todo/portlets/my_weather_portlet.pt
    create mode 100644 src/collective/todo/portlets/my_weather_portlet.py
    create mode 100644 src/collective/todo/tests/test_my_weather_portlet.py

    Generated file structure at /Users/akshay/plone/collective.todo
