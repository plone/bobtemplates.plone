
import glob
import os
import os.path
import subprocess


def generate_plone_addon_template(path,
                                  root_namespace,
                                  nested_namespace,
                                  name
                                  ):
    template = """[variables]
package.type = Basic
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

plone.version = 5-latest
""".format(root_namespace=root_namespace,
           nested_namespace=nested_namespace,
           name=name)
    with open(os.path.join(path, 'answers.ini'), 'w') as f:
        f.write(template)


base_files = [
    '.editorconfig',
    'setup.py',
    'setup.cfg',
]


addon_files = [
    'src/__init__.py'
]


def test_plone_addon_generation(tmpdir):
    generate_plone_addon_template(tmpdir.strpath, 'collective', '', 'foo')
    result = subprocess.call(
        ['mrbob', '-O', 'collective.foo', 'bobtemplates:plone_addon',
         '--config', 'answers.ini'], cwd=tmpdir.strpath
    )
    assert result == 0
    generated_files = glob.glob(tmpdir.strpath + '/collective.foo/*')
    length = len(tmpdir.strpath + '/collective.foo/')
    generated_files = [f[length:] for f in generated_files]
    required_files = base_files + addon_files
    assert required_files <= generated_files
