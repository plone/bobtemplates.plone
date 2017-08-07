# -*- coding: utf-8 -*-

import glob
import os
import os.path
import subprocess


def generate_plone_addon_template(
    path,
    root_namespace='collective',
    nested_namespace='',
    name='foo',
    version='5.1-latest'
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


base_files = [
    '.editorconfig',
    'setup.py',
    'setup.cfg',
]


addon_files = [
    'src/__init__.py',
]


def test_plone_addon_generation(tmpdir):
    generate_plone_addon_template(
        tmpdir.strpath,
        root_namespace='collective',
        nested_namespace='',
        name='foo',
        version='5.1-latest',
    )
    result = subprocess.call(
        [
            'mrbob',
            '-O', 'collective.foo',
            'bobtemplates:plone_addon',
            '--config', 'answers.ini',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0
    generated_files = glob.glob(tmpdir.strpath + '/collective.foo/*')
    length = len(tmpdir.strpath + '/collective.foo/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files
    test_result = subprocess.Popen(
        [
            'exit 0',  # replace with test command invocation.
        ],
        cwd=os.path.abspath(os.path.join(tmpdir.strpath, 'collective.foo'))
    )
    assert test_result == 0  # Tests passed without error.


def test_plone_addon_nested_generation(tmpdir):
    generate_plone_addon_template(
        tmpdir.strpath,
        root_namespace='collective',
        nested_namespace='foo',
        name='bar',
        version='5.1-latest',
    )
    result = subprocess.call(
        [
            'mrbob',
            '-O', 'collective.foo.bar',
            'bobtemplates:plone_addon',
            '--config', 'answers.ini',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0
    generated_files = glob.glob(tmpdir.strpath + '/collective.foo.bar/*')
    length = len(tmpdir.strpath + '/collective.foo.bar/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files


def test_plone_theme_generation(tmpdir):
    generate_plone_addon_template(tmpdir.strpath, 'collective', '', 'foo')
    result = subprocess.call(
        [
            'mrbob',
            '-O', 'collective.theme',
            'bobtemplates:plone_theme_package',
            '--config', 'answers.ini',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0
    generated_files = glob.glob(tmpdir.strpath + '/collective.theme/*')
    length = len(tmpdir.strpath + '/collective.theme/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files
