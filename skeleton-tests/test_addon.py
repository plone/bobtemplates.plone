# -*- coding: utf-8 -*-

from base import file_exists
from base import generate_answers_ini
from base import run_skeleton_tox_env

import glob
import os.path
import subprocess


base_files = [
    '.editorconfig',
    'setup.py',
    'setup.cfg',
    'bobtemplate.cfg',
]


addon_files = [
    'src/__init__.py',
]


def test_addon(tmpdir, capsys, config):
    template = """[variables]
package.description = Dummy package
package.example = True
package.git.init = True

author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective

plone.version = {version}
""".format(
        version=config.version,
    )
    generate_answers_ini(tmpdir.strpath, template)

    config.template = 'addon'
    config.package_name = 'collective.task'

    result = subprocess.call(
        [
            'mrbob',
            '-O', config.package_name,
            'bobtemplates.eea:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0

    generated_files = glob.glob(
        tmpdir.strpath + '/' + config.package_name + '/*',
    )
    length = len(tmpdir.strpath + '/' + config.package_name + '/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files

    base_path = tmpdir.strpath + '/' + config.package_name

    assert file_exists(base_path, '/src/collective/task/configure.zcml')

    wd = os.path.abspath(
        os.path.join(tmpdir.strpath, config.package_name),
    )

    with capsys.disabled():
        run_skeleton_tox_env(wd, config)
