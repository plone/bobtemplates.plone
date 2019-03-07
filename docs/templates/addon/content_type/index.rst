=========================
Content Type sub-template
=========================

.. topic:: Description

    Adding a Dexterity Content Type to an existing add-on package.


With this sub-template, you can add a `Dexterity <https://docs.plone.org/develop/plone/content/dexterity.html#dexterity>`_ Content Type to a Plone package.

First create a Plone add-on package:

.. code-block:: shell

    plonecli create addon ./collective.todolist

or without the ``plonecli``:

.. code-block:: shell

    mrbob bobtemplates.plone:addon -O collective.todolist

then change into the created folder ``collective.todolist`` and create your first Content Type:

.. code-block:: shell

    plonecli add content_type

or without the ``plonecli``

.. code-block:: shell

    mrbob bobtemplates.plone:content_type

It will ask you about the name of your Content Type and will use this name also for classes, interfaces. You also have the choice of using the XML supermodel or the zope.schema to define the models. The default base class is Container, but you can choose also Item. By default the template will create a class for every content type, but you can decide to use the generic Dexterity classes if you don't need your own content type classes.


Example
=======

.. code-block:: shell

    $ cd collective.todolist


Add a container Content Type
----------------------------

.. code-block:: shell

    $ plonecli add content_type

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.



    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: Todo List

    --> Content type description: A todo list

    --> Use XML Model [y]:

    --> Dexterity base class (Container/Item) [Container]:

    --> Should the content type globally addable? [n]: y

    --> Should we filter content types to be added to this container? [y]:

    --> Create a content type class [y]:

    --> Activate default behaviors? [y]:


    Should we run?:
    git add .
    git commit -m "Add content_type: Todo List"
    in: /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist
    [y]/n:
    RUN: git add .
    RUN: git commit -m "Add content_type: Todo List"
    [master 5cb2b99] "Add content_type: Todo List"
    11 files changed, 329 insertions(+), 1 deletion(-)
    create mode 100644 src/collective/todolist/content/__init__.py
    create mode 100644 src/collective/todolist/content/todo_list.py
    create mode 100644 src/collective/todolist/content/todo_list.xml
    create mode 100644 src/collective/todolist/profiles/default/types.xml
    create mode 100644 src/collective/todolist/profiles/default/types/Todo_List.xml
    create mode 100644 src/collective/todolist/tests/robot/test_ct_todo_list.robot
    create mode 100644 src/collective/todolist/tests/test_ct_todo_list.py

    Generated file structure at /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist


Add an item Content Type
------------------------

.. code-block:: shell

    $ plonecli add content_type

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.



    RUN: git status --porcelain --ignore-submodules
    Git state is clean.

    --> Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: Todo List Item

    --> Content type description: A todo list item

    --> Use XML Model [y]:

    --> Dexterity base class (Container/Item) [Container]: Item

    --> Should the content type globally addable? [n]:

    --> Parent container name [my_parent_container_type]: Todo List

    --> Create a content type class [y]:

    --> Activate default behaviors? [y]: n


    ('profile-plone.app.dexterity:default already in metadata.xml, skip adding!',)
    Should we run?:
    git add .
    git commit -m "Add content_type: Todo List Item"
    in: /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist
    [y]/n:
    RUN: git add .
    RUN: git commit -m "Add content_type: Todo List Item"
    [master 5226adf] "Add content_type: Todo List Item"
    10 files changed, 310 insertions(+), 1 deletion(-)
    create mode 100644 src/collective/todolist/content/todo_list_item.py
    create mode 100644 src/collective/todolist/content/todo_list_item.xml
    create mode 100644 src/collective/todolist/profiles/default/types.xml.example
    create mode 100644 src/collective/todolist/profiles/default/types/Todo_List_Item.xml
    create mode 100644 src/collective/todolist/tests/robot/test_ct_todo_list_item.robot
    create mode 100644 src/collective/todolist/tests/test_ct_todo_list_item.py

    Generated file structure at /home/maik/develop/src/bobtemplates.plone/tmp/collective.todolist
