# -*- coding: utf-8 -*-

from collections import namedtuple

import glob
import os
import os.path
import platform
import pytest
import subprocess
import sys


def generate_plone_addon_template(
    path,
    root_namespace='collective',
    nested_namespace='',
    name='foo',
    version='5.1-latest',
):
    template = """[variables]
package.type = Basic
theme.name = Test Theme
package.dexterity_type_name =
package.namespace = {root_namespace}
package.namespace2 = {nested_namespace}
package.name = {name}
package.description = Dummy package
package.example = True

author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective
author.irc = irc.freenode.org#plone

plone.version = {version}
""".format(
        root_namespace=root_namespace,
        nested_namespace=nested_namespace,
        name=name,
        version=version,
    )
    with open(os.path.join(path, 'answers.ini'), 'w') as f:
        f.write(template)


TestCase = namedtuple(
    'TestCase',
    [
        'template',
        'package_name',
        'root_namespace',
        'nested_namespace',
        'name',
    ],
)

base_files = [
    '.editorconfig',
    'setup.py',
    'setup.cfg',
]


addon_files = [
    'src/__init__.py',
]


@pytest.mark.skipif(
    sys.version_info >= (3, 0) or
    platform.python_implementation() != 'CPython',
    reason='Plone 4.3/5.0/5.1 currently only supports Python 2.7 on CPython.',
)
@pytest.mark.parametrize(
    'version',
    [
        '4.3-latest',
        '5.0-latest',
        '5.1-latest',
    ],
)
@pytest.mark.parametrize(
    'skeleton',
    [
        TestCase(
            template='plone_addon',
            package_name='collective.foo',
            root_namespace='collective',
            nested_namespace='',
            name='foo',
        ),
        TestCase(
            template='plone_addon',
            package_name='collective.foo.bar',
            root_namespace='collective',
            nested_namespace='foo',
            name='bar',
        ),
        TestCase(
            template='plone_theme_package',
            package_name='collective.theme',
            root_namespace='collective',
            nested_namespace='',
            name='theme',
        ),
        TestCase(
            template='plone_fattheme_buildout',
            package_name='collective.fattheme',
            root_namespace='collective',
            nested_namespace='',
            name='fattheme',
        ),
    ],
)
def test_plone_skeleton_generation(tmpdir, capsys, version, skeleton):
    generate_plone_addon_template(
        tmpdir.strpath,
        root_namespace=skeleton.root_namespace,
        nested_namespace=skeleton.nested_namespace,
        name=skeleton.name,
        version=version,
    )
    result = subprocess.call(
        [
            'mrbob',
            '-O', skeleton.package_name,
            'bobtemplates:' + skeleton.template,
            '--config', 'answers.ini',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0
    generated_files = glob.glob(
        tmpdir.strpath + '/' + skeleton.package_name + '/*',
    )
    length = len(tmpdir.strpath + '/' + skeleton.package_name + '/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files
    wd = os.path.abspath(os.path.join(tmpdir.strpath, skeleton.package_name))

    with capsys.disabled():
        bootstrap_result = subprocess.call(
            [
                'python', 'bootstrap-buildout.py',
                '--buildout-version', '2.8.0',
                '--setuptools-version', '33.1.1',
            ],
            cwd=wd,
        )
        assert bootstrap_result == 0
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
