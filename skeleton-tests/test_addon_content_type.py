# -*- coding: utf-8 -*-

from base import file_exists
from base import generate_answers_ini
from base import run_skeleton_tox_env

import os.path
import subprocess


def test_addon_content_type(tmpdir, capsys, config):
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

plone.version = {version}
""".format(
        version=config.version,
    )
    generate_answers_ini(package_dir, template)

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'collective.task'
    try:
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
    except Exception as e:
        print(e)
    assert result == 0

    wd = os.path.abspath(
        os.path.join(tmpdir.strpath, config.package_name),
    )

    # generate subtemplate content_type:
    template = """[variables]
dexterity_type_name=Tasks Container
dexterity_type_base_class=Container
dexterity_type_create_class=True
dexterity_type_global_allow=True
dexterity_type_filter_content_types=True
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(package_dir, template)

    config.template = 'content_type'
    try:
        result = subprocess.call(
            [
                'mrbob',
                'bobtemplates.eea:' + config.template,
                '--config', answers_init_path,
                '--non-interactive',
            ],
            cwd=wd,
        )
    except Exception as e:
        print(e)
    assert result == 0

    # generate 2. subtemplate content_type with Item instead of Container:
    template = """[variables]
dexterity_type_name=Task Item
dexterity_type_desc=A task Task content type for Plone
dexterity_type_supermodel=True
dexterity_type_base_class=Item
dexterity_type_create_class=True
dexterity_type_global_allow=False
dexterity_parent_container_type_name=Tasks Container
dexterity_type_activate_default_behaviors=False
"""
    generate_answers_ini(package_dir, template)

    config.template = 'content_type'
    try:
        result = subprocess.call(
            [
                'mrbob',
                'bobtemplates.eea:' + config.template,
                '--config', answers_init_path,
                '--non-interactive',
            ],
            cwd=wd,
        )
    except Exception as e:
        print(e)
    assert result == 0

    assert file_exists(wd, '/src/collective/task/configure.zcml')

    with capsys.disabled():
        run_skeleton_tox_env(wd, config)
