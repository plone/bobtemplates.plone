# -*- coding: utf-8 -*-

from base import dummy_contextmanager
from base import file_exists
from base import generate_answers_ini

import os.path
import subprocess


def test_behavior(tmpdir, capsys, config):
    template = """[variables]
package.description = Dummy package
package.example = True

author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective

plone.version = {version}
""".format(
        version=config.version,
    )
    generate_answers_ini(tmpdir.strpath, template)

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'collective.todo'
    result = subprocess.call(
        [
            'mrbob',
            '-O', config.package_name,
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0

    wd = os.path.abspath(
        os.path.join(tmpdir.strpath, config.package_name),
    )

    # generate subtemplate content_type:
    template = """[variables]
vocabulary_name = AvailableTodos
subtemplate_warning = Yes
"""
    generate_answers_ini(wd, template)

    config.template = 'behavior'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/todo/vocabularies/configure.zcml')
    assert file_exists(
        wd, '/src/collective/todo/vocabularies/available_todos.py')  # NOQA: S101,E501

    with capsys.disabled() if config.verbose else dummy_contextmanager():
        setup_virtualenv_result = subprocess.call(
            [
                'virtualenv',
                '.',
            ],
            cwd=wd,
        )
        assert setup_virtualenv_result == 0
        install_buildout_result = subprocess.call(
            [
                './bin/pip',
                'install',
                '-U',
                '-r',
                'requirements.txt',
            ],
            cwd=wd,
        )
        assert install_buildout_result == 0
        annotate_result = subprocess.call(
            ['bin/buildout', 'annotate', ],
            cwd=wd,
        )
        assert annotate_result == 0
        buildout_result = subprocess.call(
            ['bin/buildout', ],
            cwd=wd,
        )
        assert buildout_result == 0
        test_result = subprocess.call(
            ['bin/test', ],
            cwd=wd,
        )
        assert test_result == 0
        test__code_convention_result = subprocess.call(
            ['bin/code-analysis', ],
            cwd=wd,
        )
        assert test__code_convention_result == 0
