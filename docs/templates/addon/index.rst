===============
Add-on template
===============

.. topic:: Description

    Creating an add-on package and extending it with  sub-template's.

..  toctree::
    :maxdepth: 1
    :glob:

    */index

With this template you can create a basic Plone package.

.. code-block:: shell

    mrbob -O collective.todos bobtemplates.plone:addon

This will create a Python package for you, which you can extend manually or by using other sub-templates like ``theme`` or ``content_type`` from bobtemplates.plone.

Example
=======

.. code-block:: shell

    $ mrbob bobtemplates.plone:addon -O collective.todolist

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.


    --> Package description [An add-on for Plone]: A todo list add-on for Plone

    --> Do you want me to initialze a GIT repository in your new package? (y/n) [y]:


    RUN: git init
    Leeres Git-Repository in /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist/.git/ initialisiert

    Should we run?:
    git add .
    git commit -m "Create addon: collective.todolist"
    in: /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist
    [y]/n:
    RUN: git add .
    RUN: git commit -m "Create addon: collective.todolist"
    [master (Basis-Commit) 04b6727] "Create addon: collective.todolist"
    48 files changed, 1381 insertions(+)
    create mode 100644 .coveragerc
    create mode 100644 .editorconfig
    create mode 100644 .gitattributes
    create mode 100644 .gitignore
    create mode 100644 .gitlab-ci.yml
    create mode 100644 .travis.yml
    create mode 100644 CHANGES.rst
    create mode 100644 CONTRIBUTORS.rst
    create mode 100644 DEVELOP.rst
    create mode 100644 LICENSE.GPL
    create mode 100644 LICENSE.rst
    create mode 100644 MANIFEST.in
    create mode 100644 README.rst
    create mode 100644 bobtemplate.cfg
    create mode 100644 buildout.cfg
    create mode 100644 docs/index.rst
    create mode 100644 requirements.txt
    create mode 100644 setup.cfg
    create mode 100644 setup.py
    create mode 100644 src/collective/__init__.py
    create mode 100644 src/collective/todolist/__init__.py
    create mode 100644 src/collective/todolist/browser/__init__.py
    create mode 100644 src/collective/todolist/browser/configure.zcml
    create mode 100644 src/collective/todolist/browser/overrides/.gitkeep
    create mode 100644 src/collective/todolist/browser/static/.gitkeep
    create mode 100644 src/collective/todolist/configure.zcml
    create mode 100644 src/collective/todolist/interfaces.py
    create mode 100644 src/collective/todolist/locales/README.rst
    create mode 100644 src/collective/todolist/locales/__init__.py
    create mode 100644 src/collective/todolist/locales/collective.todolist.pot
    create mode 100644 src/collective/todolist/locales/en/LC_MESSAGES/collective.todolist.po
    create mode 100644 src/collective/todolist/locales/update.py
    create mode 100755 src/collective/todolist/locales/update.sh
    create mode 100644 src/collective/todolist/permissions.zcml
    create mode 100644 src/collective/todolist/profiles/default/browserlayer.xml
    create mode 100644 src/collective/todolist/profiles/default/catalog.xml
    create mode 100644 src/collective/todolist/profiles/default/metadata.xml
    create mode 100644 src/collective/todolist/profiles/default/registry.xml
    create mode 100644 src/collective/todolist/profiles/default/rolemap.xml
    create mode 100644 src/collective/todolist/profiles/uninstall/browserlayer.xml
    create mode 100644 src/collective/todolist/setuphandlers.py
    create mode 100644 src/collective/todolist/testing.py
    create mode 100644 src/collective/todolist/tests/__init__.py
    create mode 100644 src/collective/todolist/tests/robot/test_example.robot
    create mode 100644 src/collective/todolist/tests/test_robot.py
    create mode 100644 src/collective/todolist/tests/test_setup.py
    create mode 100644 src/collective/todolist/upgrades.py
    create mode 100644 src/collective/todolist/upgrades.zcml

    Generated file structure at /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist
