===========
GIT-Support
===========

Since 3.2.x bobtemplates.plone has integrated GIT support and can check for clean repository state, initialize a GIT repository for a new created package and commit all changes a template is making.

For your convenience, you can set some defaults in your mrbob user configuration

.. code-block:: shell

    cat ~/.mrbob

    [mr.bob]
    verbose = False

    [variables]
    author.name = Maik Derstappen
    author.email = md@derico.de
    author.github.user = MrTango
    plone.version = 5.1-latest
    package.git.init = True
    package.git.autocommit = True
    package.git.disabled = False

This will allow you to define if you want to allways git initialize a created package and do a commit after every sub-templates was rendered, without asking all the time. You can even disable the git support completely if you need to.


Example configurations
======================

Default
-------

If you don't set any default values, the default answers of the questions are as follows.

You will be questioned for ``git init`` and ``git auto commit``, by default they are set to YES. But you can always switch them to No.

Fix settings
------------

If you always work the same, you can set these answers in your .mrbob file and you will not be ask all the time.

::

    package.git.init: True
    package.git.autocommit: True


Disable git init
----------------

In case you are don't want an extra git repository for every package you create, but use a parent project based repository, you can disable the git init, by setting ``package.git.init`` to ``False``.

::

   package.git.init = False

Disable git support completely
------------------------------

To disable the GIT support completely, set ``package.git.disable`` to ``True``. But it's hightly recommended to let it active, because sub-templates can silendly override files. **So be warned!**

::

   package.git.disabled = True
