# -*- coding: utf-8 -*-

import base
import glob
import os.path
import subprocess


base_files = [
    '.editorconfig',
    'setup.py',
    'setup.cfg',
]


addon_files = [
    'src/__init__.py',
    'src/plonetheme/blacksea/theme/manifest.cfg',
]


def test_theme_package(tmpdir, capsys, config):
    template = """[variables]
package.description = Dummy package
theme.name = Black Sea theme
author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective
subtemplate_warning=False
package.git.init = True

plone.version = {version}
""".format(
        version=config.version,
    )
    base.generate_answers_ini(tmpdir.strpath, template)

    config.template = 'theme_package'
    config.package_name = 'plonetheme.blacksea'

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

    assert base.file_exists(
        base_path,
        '/src/plonetheme/blacksea/theme/manifest.cfg',
    )

    wd = os.path.abspath(
        os.path.join(tmpdir.strpath, config.package_name),
    )

    with capsys.disabled():
        try:
            test_result = subprocess.check_output(
                ['tox'],
                cwd=wd,
            )
            print('\n{0}\n'.format(test_result.decode('utf-8')))
        except subprocess.CalledProcessError as execinfo:
            tox_msg = b''.join(
                execinfo.output.partition(b'__ summary __')[1:],
            ).decode()
            assert execinfo.returncode == 0, '\n{0}'.format(tox_msg)
