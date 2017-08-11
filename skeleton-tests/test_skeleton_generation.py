# -*- coding: utf-8 -*-

import contextlib
import glob
import os
import os.path
import subprocess


@contextlib.contextmanager
def dummy_contextmanager():
    yield None


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


base_files = [
    '.editorconfig',
    'setup.py',
    'setup.cfg',
]


addon_files = [
    'src/__init__.py',
]


def test_plone_skeleton_generation(tmpdir, capsys):
    verbose = bool(os.environ.get('VERBOSE'))
    version = os.environ.get('VERSION', '5.1-latest')
    template = os.environ.get('TEMPLATE')
    package_name = os.environ.get('PACKAGENAME', 'collective.foo')
    namespace_elements = package_name.split('.')
    root_namespace = namespace_elements[0]
    name = namespace_elements[:-1]
    nested_namespace = ''
    if len(namespace_elements) == 3:
        nested_namespace = namespace_elements[1]

    generate_plone_addon_template(
        tmpdir.strpath,
        root_namespace=root_namespace,
        nested_namespace=nested_namespace,
        name=name,
        version=version,
    )
    result = subprocess.call(
        [
            'mrbob',
            '-O', package_name,
            'bobtemplates:' + template,
            '--config', 'answers.ini',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0
    generated_files = glob.glob(
        tmpdir.strpath + '/' + package_name + '/*',
    )
    length = len(tmpdir.strpath + '/' + package_name + '/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files
    wd = os.path.abspath(os.path.join(tmpdir.strpath, package_name))

    with capsys.disabled() if verbose else dummy_contextmanager():
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
