# -*- coding: utf-8 -*-

from base import dummy_contextmanager
from base import file_exists
from base import generate_answers_ini

import os.path
import subprocess


def test_addon_view(tmpdir, capsys, config):
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
    generate_answers_ini(tmpdir.strpath, template)

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'collective.sample'
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

    assert file_exists(wd, '/src/collective/sample/configure.zcml')

    with capsys.disabled() if config.verbose else dummy_contextmanager():
        try:
            test_result = subprocess.check_output(
                ['tox'],
                cwd=wd,
            )
            print(">>>>>>\n{0}\n>>>>>>\n".format(test_result.decode('utf-8')))
        except subprocess.CalledProcessError as execinfo:
            tox_msg = b''.join(
                execinfo.output.partition(b'__ summary __')[1:],
            ).decode()
            assert execinfo.returncode == 0, tox_msg
