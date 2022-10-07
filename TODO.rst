Templates to build
==================

Sub-templates
-------------

- controlpanel
- mosaic tile
- global utility (almost the same as vocabulary)???
- local utility (persistent utility)???
- souper.plone ???
- z3c.form default values
- display widget templates

Standalone-templates
--------------------

- docker?


Notes
=====

Content type name check
-----------------------

Check content_type name, to not conflict with common content types in Plone.


Improve git/hg support
----------------------

We want to replace the first question with a git/hg check for a clean state a the repository. If the state is clean continue with the qiestions, if not exit with a message.

It would be nice to have an auto commit after using a bobtemplate. For example, after using the ``content_type`` sub-template to create a content type named "Todo Task", we could make a ``git add .`` and ``git commit -m "Add content_type Todo Tasks"``. This way we can easily revert the change later.
