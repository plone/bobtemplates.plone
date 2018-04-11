===========
GIT-Support
===========

Since 3.2.x bobtemplates.plone has integrated GIT support and can check for clean repository state, initialize a GIT repository for a new created package and commit all changes a template is making.

For your convenience, you can set some defaults in your mrbob user configuration

.. code-block:: sh

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
