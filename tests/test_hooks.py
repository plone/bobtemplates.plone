# -*- coding: utf-8 -*-
from bobtemplates import hooks
from mrbob.bobexceptions import TemplateConfigurationError
from mrbob.bobexceptions import ValidationError
from mrbob.configurator import Configurator

import glob
import os
import os.path
import pytest
import subprocess
import unittest


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


def generate_mrbob_ini(path):
    template = """[Questions]
""".format()
    with open(os.path.join(path, '.mrbob.ini'), 'w') as f:
        f.write(template)


base_files = [
    '.mrbob.ini',
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


def test_to_boolean():
    # Initial simple test to show coverage in hooks.py.
    assert hooks.to_boolean(None, None, 'y')
    assert hooks.to_boolean(None, None, 'yes')
    assert hooks.to_boolean(None, None, 'true')
    assert hooks.to_boolean(None, None, '1')
    assert hooks.to_boolean(None, None, 'n') is False
    assert hooks.to_boolean(None, None, 'no') is False
    assert hooks.to_boolean(None, None, 'false') is False
    assert hooks.to_boolean(None, None, '0') is False
    with pytest.raises(ValidationError, msg='Value must be a boolean (y/n)'):
        assert hooks.to_boolean(None, None, 'spam')


def test_post_dexterity_type_name():
    """Test validation of entered dexterity type names
    """
    def hookit(value):
        return hooks.post_dexterity_type_name(None, None, value)

    with pytest.raises(ValidationError):
        hookit('import')
    with pytest.raises(ValidationError):
        hookit(u'süpertype')
    with pytest.raises(ValidationError):
        hookit(u'Staff Member')
    with pytest.raises(ValidationError):
        hookit(u'2ndComing')
    with pytest.raises(ValidationError):
        hookit(u'Second Coming')
    with pytest.raises(ValidationError):
        hookit(u'Staff Member')
    with pytest.raises(ValidationError):
        hookit(u'*sterisk')
    assert hookit(u'Supertype') == u'Supertype'
    assert hookit(u'second_coming') == u'second_coming'
    assert hookit(u'the_2nd_coming') == u'the_2nd_coming'


# @pytest.mark.usefixtures("tmpdir")
class PloneAddTest(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        tmpdir.chdir()

    def setUp(self):
        generate_plone_addon_template('.', 'collective', '', 'foo')
        result = subprocess.call(
            ['mrbob', '-O', 'collective.foo', 'bobtemplates:plone_addon',
             '--config', 'answers.ini']
        )
        assert result == 0

    def test_validate_packagename(self):
        with pytest.raises(AttributeError):
            hooks.validate_packagename(None)

        with pytest.raises(TemplateConfigurationError,
                           msg=""):
            configurator = Configurator(
                template='collective.foo',
                target_directory='.')

        generate_mrbob_ini('./collective.foo/')
        configurator = Configurator(
            template='collective.foo',
            target_directory='.')

        with pytest.raises(SystemExit):
            hooks.validate_packagename(configurator)
