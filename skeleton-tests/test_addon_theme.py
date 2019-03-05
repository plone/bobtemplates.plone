# -*- coding: utf-8 -*-

from base import file_exists
from base import generate_answers_ini
from bobtemplates.plone.utils import safe_unicode

import os.path
import subprocess


def test_addon_theme(tmpdir, capsys, config):
    answers_init_path = os.path.join(tmpdir.strpath, 'answers.ini')
    package_dir = os.path.abspath(
        tmpdir.strpath,
    )
    template = """[variables]
package.description = Dummy package

author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective
subtemplate_warning=False
package.git.init = True

plone.version = {version}
""".format(
        version=config.version,
    )
    generate_answers_ini(package_dir, template)

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'plonetheme.task'
    result = subprocess.call(
        [
            'mrbob',
            '-O', config.package_name,
            'bobtemplates.plone:' + config.template,
            '--config', answers_init_path,
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

    assert file_exists(wd, '/src/plonetheme/task/theme/manifest.cfg')

    with capsys.disabled():
        try:
            test_result = subprocess.check_output(
                ['tox', '-e', config.skeleton_tox_env],
                cwd=wd,
            )
            print('\n{0}\n'.format(test_result.decode('utf-8')))
        except subprocess.CalledProcessError as execinfo:
            tox_msg = safe_unicode(b''.join(
                execinfo.output,
            ))
            print(tox_msg)
            tox_summary = safe_unicode(b''.join(
                execinfo.output.partition(b'__ summary __')[1:],
            ))
            assert execinfo.returncode == 0, '\n{0}'.format(tox_summary)
