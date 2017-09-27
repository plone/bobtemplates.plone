Using the development buildout
------------------------------

Create a virtualenv in the package

.. code-block:: console

    $ virtualenv --clear .

Install requirements with pip

.. code-block:: console

    $ ./bin/pip install -r requirements.txt

Run buildout

.. code-block:: console

    $ ./bin/buildout

Start Plone in foreground

.. code-block:: console

    $ ./bin/instance fg
