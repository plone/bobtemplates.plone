# -*- coding: utf-8 -*-

from base import file_exists
from base import generate_answers_ini
from base import run_skeleton_tox_env

import os.path
import subprocess


def test_addon_viewlet(tmpdir, capsys, config):
    answers_init_path = os.path.join(tmpdir.strpath, 'answers.ini')
    package_dir = os.path.abspath(
        tmpdir.strpath,
    )
    template = """[variables]
package.description = Dummy package
package.example = True
package.git.init = True
author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective
package.git.autocommit = True
plone.version = {version}
""".format(
        version=config.version,
    )
    generate_answers_ini(package_dir, template)

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'collective.task'
    result = subprocess.call(
        [
            'mrbob',
            '-O', config.package_name,
            'bobtemplates.eea:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0

    wd = os.path.abspath(
        os.path.join(tmpdir.strpath, config.package_name),
    )

    # generate subtemplate viewlet:
    template = """[variables]
subtemplate_warning=True
viewlet_name=first_viewlet
viewlet_python_class_name=MyView
viewlet_template=True
viewlet_template_name=pt_viewlet
"""
    generate_answers_ini(package_dir, template)

    config.template = 'viewlet'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.eea:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    # generate subtemplate viewlet:
    template = """[variables]
subtemplate_warning=True
viewlet_name=second_viewlet
viewlet_python_class_name=DemoView
viewlet_template=False
"""
    generate_answers_ini(wd, template)

    config.template = 'viewlet'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.eea:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/configure.zcml')

    with capsys.disabled():
        run_skeleton_tox_env(wd, config)
