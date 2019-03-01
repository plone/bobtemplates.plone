# -*- coding: utf-8 -*-

from base import dummy_contextmanager
from base import file_exists
from base import generate_answers_ini

import os.path
import subprocess


def test_addon_content_type(tmpdir, capsys, config):
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

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'collective.task'
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
dexterity_type_name=Tasks Container
dexterity_type_base_class=Container
dexterity_type_create_class=True
dexterity_type_global_allow=True
dexterity_type_filter_content_types=True
subtemplate_warning=False
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate 2. subtemplate content_type with Item instead of Container:
    template = """[variables]
dexterity_type_name=Task Item
dexterity_type_base_class=Item
dexterity_type_create_class=True
dexterity_type_global_allow=True
subtemplate_warning=True
dexterity_type_desc=A task Task content type for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate subtemplate content_type with generic class:
    template = """[variables]
dexterity_type_name=Generic Tasks Container
dexterity_type_base_class=Container
dexterity_type_create_class=False
dexterity_type_global_allow=True
dexterity_type_filter_content_types=False
subtemplate_warning=True
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate subtemplate content_type with generic class:
    template = """[variables]
dexterity_type_name=Task Item Python Schema
dexterity_type_base_class=Item
dexterity_type_create_class=True
dexterity_type_global_allow=True
dexterity_type_filter_content_types=False
subtemplate_warning=True
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=False
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate subtemplate content_type with parent container:
    template = """[variables]
dexterity_type_name=Parent
dexterity_type_base_class=Container
dexterity_type_create_class=True
dexterity_type_global_allow=True
dexterity_type_filter_content_types=True
subtemplate_warning=True
dexterity_type_desc=A parent container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate subtemplate content_type with child container:
    template = """[variables]
dexterity_type_name=Child
dexterity_type_base_class=Item
dexterity_type_create_class=True
dexterity_type_global_allow=False
dexterity_parent_container_type_name=Parent
dexterity_type_filter_content_types=False
subtemplate_warning=True
dexterity_type_desc=A child container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate subtemplate content_type:
    template = """[variables]
dexterity_type_name=News Container
dexterity_type_base_class=Container
dexterity_type_create_class=True
dexterity_type_global_allow=y
dexterity_type_filter_content_types=n
subtemplate_warning=False
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    # generate subtemplate content_type:
    template = """[variables]
dexterity_type_name=Another Container
dexterity_type_base_class=Container
dexterity_type_create_class=True
dexterity_type_global_allow=1
dexterity_type_filter_content_types=y
subtemplate_warning=False
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=True
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
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

    assert file_exists(wd, '/src/collective/task/configure.zcml')

    with capsys.disabled() if config.verbose else dummy_contextmanager():
        try:
            test_result = subprocess.check_output(
                ['tox'],
                cwd=wd,
            )
            print(test_result)
        except subprocess.CalledProcessError as execinfo:
            print(execinfo.output)
            assert 'failed' in execinfo
