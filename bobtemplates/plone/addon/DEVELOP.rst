Using the development buildout
==============================

plonecli
--------

The convenient way, use plonecli build ;)::

    $ plonecli build

or with --clear if you want to clean your existing venv::

    $ plonecli build --clear

Start your instance::

    $ plonecli serve


Without plonecli
----------------

Create a virtualenv in the package::

    $ python3 -m venv venv

or with --clear if you want to clean your existing venv::

    $ python3 -m venv venv --clear

Install requirements with pip::

    $ ./venv/bin/pip install -r requirements.txt

bootstrap your buildout::

    $ ./bin/buildout bootstrap

Run buildout::

    $ ./bin/buildout

Start Plone in foreground::

    $ ./bin/instance fg


Running tests
-------------

    $ tox

list all tox environments::

    $ tox -l
    py27-Plone43
    py27-Plone51
    py27-Plone52
    py37-Plone52
    build_instance
    code-analysis
    lint-py27
    lint-py37
    coverage-report

run a specific tox env::

    $ tox -e py37-Plone52


CI Github-Actions / codecov
---------------------------

The first time you push the repo to github, you might get an error from codecov.
Either you activate the package here: `https://app.codecov.io/gh/collective/+ <https://app.codecov.io/gh/collective/+>`_
Or you just wait a bit, codecov will activate your package automatically.
