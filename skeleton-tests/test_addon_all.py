# -*- coding: utf-8 -*-

from base import file_exists
from base import generate_answers_ini
from base import run_skeleton_tox_env

import os.path
import subprocess


def test_addon_all(tmpdir, capsys, config):
    answers_init_path = os.path.join(tmpdir.strpath, "answers.ini")
<<<<<<< HEAD
    package_dir = os.path.abspath(tmpdir.strpath)
=======
    package_dir = os.path.abspath(tmpdir.strpath,)
>>>>>>> refactor test setup, run most skeleton test in at once, apply isort to more templates
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
    config.template = "addon"
    config.package_name = "collective.task"
    try:
        result = subprocess.call(
            [
                "mrbob",
                "-O",
                config.package_name,
                "bobtemplates.plone:" + config.template,
                "--config",
                answers_init_path,
                "--non-interactive",
            ],
            cwd=tmpdir.strpath,
        )
    except Exception as e:
        print(e)
    assert result == 0

<<<<<<< HEAD
    wd = os.path.abspath(os.path.join(tmpdir.strpath, config.package_name))
=======
    wd = os.path.abspath(os.path.join(tmpdir.strpath, config.package_name),)
>>>>>>> refactor test setup, run most skeleton test in at once, apply isort to more templates

    # generate subtemplate content_type:
    template = """[variables]
dexterity_type_name=Tasks Container
dexterity_type_base_class=Container
dexterity_type_create_class=True
dexterity_type_global_allow=True
dexterity_type_filter_content_types=True
dexterity_type_desc=A tasks container for Plone
dexterity_type_supermodel=False
"""
    generate_answers_ini(package_dir, template)

    config.template = "content_type"
    try:
        result = subprocess.call(
            [
                "mrbob",
                "bobtemplates.plone:" + config.template,
                "--config",
                answers_init_path,
                "--non-interactive",
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

    config.template = "content_type"
    try:
        result = subprocess.call(
            [
                "mrbob",
                "bobtemplates.plone:" + config.template,
                "--config",
                answers_init_path,
                "--non-interactive",
            ],
            cwd=wd,
        )
    except Exception as e:
        print(e)
    assert result == 0

    assert file_exists(wd, "/src/collective/task/configure.zcml")

    # generate subtemplate behavior:
    template = """[variables]
behavior_name = Project
subtemplate_warning = Yes
"""
    generate_answers_ini(package_dir, template)

    config.template = "behavior"
    result = subprocess.call(
        [
            "mrbob",
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_init_path,
            "--non-interactive",
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, "/src/collective/task/behaviors/configure.zcml")
    assert file_exists(
        wd, "/src/collective/task/behaviors/project.py"
    )  # NOQA: S101,E501

    # generate subtemplate indexer:
    template = """[variables]
indexer_name = my_custom_test_indexer
subtemplate_warning = Yes
"""
    generate_answers_ini(package_dir, template)

    config.template = "indexer"
    result = subprocess.call(
        [
            "mrbob",
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_init_path,
            "--non-interactive",
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, "/src/collective/task/indexers/configure.zcml")
    assert file_exists(wd, "/src/collective/task/indexers/my_custom_test_indexer.zcml")
    assert file_exists(wd, "/src/collective/task/indexers/my_custom_test_indexer.py")

    # generate subtemplate portlet:
    template = """[variables]
portlet_name=My Weather
"""
    generate_answers_ini(package_dir, template)

    config.template = "portlet"
    result = subprocess.call(
        [
            "mrbob",
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_init_path,
            "--non-interactive",
        ],
        cwd=wd,
    )
    assert result == 0

    # generate subtemplate portlet:
    template = """[variables]
portlet_name=Another Weather Portlet
"""
    generate_answers_ini(package_dir, template)

    config.template = "portlet"
    result = subprocess.call(
        [
            "mrbob",
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_init_path,
            "--non-interactive",
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, "/src/collective/task/configure.zcml")

    # generate subtemplate restapi_service:
    template = """[variables]
service_class_name=RelatedImages
service_name=related-images
"""
    generate_answers_ini(package_dir, template)

    config.template = 'restapi_service'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/configure.zcml')

    # generate subtemplate svelte_app:
    template = """[variables]
svelte_app_name = my-custom-svelte-element
svelte_app_custom_element = Yes
subtemplate_warning = Yes
"""
    generate_answers_ini(package_dir, template)

    config.template = "svelte_app"
    result = subprocess.call(
        [
            "mrbob",
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_init_path,
            "--non-interactive",
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, "/svelte_src/my-custom-svelte-element/README.md")
    assert file_exists(wd, "/src/collective/task/svelte_apps/my-custom-svelte-element/README.md")

<<<<<<< HEAD
=======
    # generate subtemplate theme:
    template = """[variables]
theme.name = Plone theme Blacksea
subtemplate_warning=False
"""
    generate_answers_ini(package_dir, template)

    config.template = 'theme'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/theme/manifest.cfg')

>>>>>>> refactor test setup, run most skeleton test in at once, apply isort to more templates
    # generate subtemplate upgrade_step:
    template = """[variables]
upgrade_step_title = reindex the thing
upgrade_step_description = Upgrade the thing
subtemplate_warning = Yes
"""
    generate_answers_ini(package_dir, template)

    config.template = "upgrade_step"
    result = subprocess.call(
        [
            "mrbob",
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_init_path,
            "--non-interactive",
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, "/src/collective/task/upgrades/configure.zcml")
    assert file_exists(wd, "/src/collective/task/upgrades/1001.zcml")
    assert file_exists(wd, "/src/collective/task/upgrades/v1001.py")

    # generate subtemplate view:
    template = """[variables]
view_python_class=True
view_python_class_name=MyView
view_name=my_view
view_template=True
view_template_name=pt_view
"""
    generate_answers_ini(package_dir, template)

    config.template = 'view'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/configure.zcml')

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
            'bobtemplates.plone:' + config.template,
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
            'bobtemplates.plone:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/configure.zcml')

    # generate subtemplate vocabulary:
    template = """[variables]
vocabulary_name = AvailableTasks
subtemplate_warning = Yes
"""
    generate_answers_ini(package_dir, template)

    config.template = 'vocabulary'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', answers_init_path,
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/vocabularies/configure.zcml')
    assert file_exists(
        wd,
        '/src/collective/task/tests/test_vocab_available_tasks.py',
    )
    assert file_exists(
        wd,
        '/src/collective/task/vocabularies/available_tasks.py',
    )

    with capsys.disabled():
        returncode = run_skeleton_tox_env(wd, config)
        assert returncode == 0, u"The tests inside the generated package are failing, please check the output above!"
