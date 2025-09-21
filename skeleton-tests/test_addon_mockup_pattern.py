from base import file_exists
from base import generate_answers_ini
from base import run_skeleton_tox_env
from mrbob.cli import main

import os
import re
import subprocess


def test_addon_pattern(tmpdir, capsys, config):
    answers_ini_path = os.path.join(tmpdir.strpath, "answers.ini")
    package_dir = os.path.abspath(tmpdir.strpath)
    template = f"""[variables]
package.description = Pattern Test Package
package.git.disabled = True

author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective
subtemplate_warning=False

plone.version = {config.version}
"""
    generate_answers_ini(package_dir, template)

    # generate template addon:
    config.template = "addon"
    config.package_name = "collective.testpattern"

    wd = os.path.abspath(os.path.join(tmpdir.strpath, config.package_name))
    result = subprocess.call(
        [
            "mrbob",
            "-O",
            config.package_name,
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_ini_path,
            "--non-interactive",
        ],
        cwd=tmpdir.strpath,
    )

    # generate subtemplate content_type:
    template = """[variables]
pattern.name = test-pattern
subtemplate_warning=False
"""
    generate_answers_ini(package_dir, template)

    config.template = "mockup_pattern"
    result = subprocess.call(
        [
            "mrbob",
            "-O",
            config.package_name,
            "bobtemplates.plone:" + config.template,
            "--config",
            answers_ini_path,
            "--non-interactive",
        ],
        cwd=tmpdir.strpath,
    )


    assert file_exists(wd, "/package.json")
    assert file_exists(wd, "/webpack.config.js")
    assert file_exists(
        wd,
        "/src/collective/testpattern/profiles/default/registry/bundles.xml",
    )
    found_jscompilation = False
    with open(
        f"{wd}/src/collective/testpattern/profiles/default/registry/bundles.xml"
    ) as bundles_file:
        for line in bundles_file.readlines():
            if "jscompilation" in line:
                value = re.search(r">([^<]*)", line)[1]
                assert value == (
                    "++plone++collective.testpattern/bundles/testpattern-remote.min.js"
                )
                found_jscompilation = True
    assert found_jscompilation

    # with capsys.disabled():
    #     run_skeleton_tox_env(wd, config)
