# -*- coding: utf-8 -*-
import unittest
import os
import tempfile
import shutil

from bobtemplates import hooks
from mrbob.bobexceptions import ValidationError
from scripttest import TestFileEnvironment


class BaseTemplateTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

        # docs http://pythonpaste.org/scripttest/
        self.env = TestFileEnvironment(
            os.path.join(self.tempdir, 'test-output'),
            ignore_hidden=False,
        )

    def create_template(self):
        """Run mr.bob to create your template."""
        options = {
            'dir': os.path.join(os.path.dirname(__file__)),
            'template': self.template,
            'project': self.project,
            'answers_file': self.answers_file,
        }
        return self.env.run(
            '%(dir)s/bin/mrbob -O %(project)s --config '
            '%(dir)s/%(answers_file)s %(dir)s/bobtemplates/%(template)s'
            % options)


class PloneTemplateTest(BaseTemplateTest):
    """Tests for the templates."""
    template = ''
    project = ''
    answers_file = ''

    def test_plone_addon_template(self):
        """Test the `plone_addon` template.

        Generate a project from a template, test which files were created
        and run all tests in the generated package.
        """
        self.template = 'plone_addon'
        self.project = 'collective.foo'
        self.answers_file = 'nosetests_answers.ini'
        self.maxDiff = None
        result = self.create_template()
        self.assertItemsEqual(
            result.files_created.keys(),
            [
                self.project,
                self.project + '/.coveragerc',
                self.project + '/.editorconfig',
                self.project + '/.gitattributes',
                self.project + '/.gitignore',
                self.project + '/.travis.yml',
                self.project + '/bootstrap-buildout.py',
                self.project + '/buildout.cfg',
                self.project + '/CHANGES.rst',
                self.project + '/CONTRIBUTORS.rst',
                self.project + '/docs',
                self.project + '/docs/index.rst',
                self.project + '/LICENSE.GPL',
                self.project + '/LICENSE.rst',
                self.project + '/MANIFEST.in',
                self.project + '/README.rst',
                self.project + '/requirements.txt',
                self.project + '/setup.cfg',
                self.project + '/setup.py',
                self.project + '/src',
                self.project + '/src/collective',
                self.project + '/src/collective/__init__.py',
                self.project + '/src/collective/foo',
                self.project + '/src/collective/foo/__init__.py',
                self.project + '/src/collective/foo/browser',
                self.project + '/src/collective/foo/browser/__init__.py',
                self.project + '/src/collective/foo/browser/configure.zcml',
                self.project + '/src/collective/foo/browser/overrides',
                self.project + '/src/collective/foo/browser/overrides/.gitkeep',  # noqa
                self.project + '/src/collective/foo/browser/static',
                self.project + '/src/collective/foo/browser/static/.gitkeep',
                self.project + '/src/collective/foo/configure.zcml',
                self.project + '/src/collective/foo/interfaces.py',
                self.project + '/src/collective/foo/locales',
                self.project + '/src/collective/foo/locales/collective.foo.pot',  # noqa
                self.project + '/src/collective/foo/locales/update.sh',
                self.project + '/src/collective/foo/profiles',
                self.project + '/src/collective/foo/profiles/default',
                self.project + '/src/collective/foo/profiles/default/browserlayer.xml',  # noqa
                self.project + '/src/collective/foo/profiles/default/metadata.xml',  # noqa
                self.project + '/src/collective/foo/profiles/default/registry.xml',  # noqa
                self.project + '/src/collective/foo/profiles/uninstall',
                self.project + '/src/collective/foo/profiles/uninstall/browserlayer.xml',  # noqa
                self.project + '/src/collective/foo/setuphandlers.py',
                self.project + '/src/collective/foo/testing.py',
                self.project + '/src/collective/foo/tests',
                self.project + '/src/collective/foo/tests/__init__.py',
                self.project + '/src/collective/foo/tests/robot',
                self.project + '/src/collective/foo/tests/robot/test_example.robot',  # noqa
                self.project + '/src/collective/foo/tests/test_robot.py',
                self.project + '/src/collective/foo/tests/test_setup.py',
            ]
        )

    def test_plone_addon_nested_template(self):
        """Test the `plone_addon_nested` template.

        Generate a project from a template, test which files were created
        and run all tests in the generated package.
        """
        self.template = 'plone_addon'
        self.project = 'collective.foo.bar'
        self.answers_file = 'nosetests_answers_nested.ini'
        self.maxDiff = None
        result = self.create_template()
        self.assertItemsEqual(
            result.files_created.keys(),
            [
                self.project,
                self.project + '/.coveragerc',
                self.project + '/.editorconfig',
                self.project + '/.gitattributes',
                self.project + '/.gitignore',
                self.project + '/.travis.yml',
                self.project + '/bootstrap-buildout.py',
                self.project + '/buildout.cfg',
                self.project + '/CHANGES.rst',
                self.project + '/CONTRIBUTORS.rst',
                self.project + '/docs',
                self.project + '/docs/index.rst',
                self.project + '/LICENSE.GPL',
                self.project + '/LICENSE.rst',
                self.project + '/MANIFEST.in',
                self.project + '/README.rst',
                self.project + '/requirements.txt',
                self.project + '/setup.cfg',
                self.project + '/setup.py',
                self.project + '/src',
                self.project + '/src/collective',
                self.project + '/src/collective/__init__.py',
                self.project + '/src/collective/foo',
                self.project + '/src/collective/foo/__init__.py',
                self.project + '/src/collective/foo/bar',
                self.project + '/src/collective/foo/bar/__init__.py',
                self.project + '/src/collective/foo/bar/browser',
                self.project + '/src/collective/foo/bar/browser/__init__.py',
                self.project + '/src/collective/foo/bar/browser/configure.zcml',  # noqa
                self.project + '/src/collective/foo/bar/browser/overrides',  # noqa
                self.project + '/src/collective/foo/bar/browser/overrides/.gitkeep',  # noqa
                self.project + '/src/collective/foo/bar/browser/static',
                self.project + '/src/collective/foo/bar/browser/static/.gitkeep',  # noqa
                self.project + '/src/collective/foo/bar/configure.zcml',
                self.project + '/src/collective/foo/bar/interfaces.py',
                self.project + '/src/collective/foo/bar/locales',
                self.project + '/src/collective/foo/bar/locales/collective.foo.bar.pot',  # noqa
                self.project + '/src/collective/foo/bar/locales/update.sh',
                self.project + '/src/collective/foo/bar/profiles',
                self.project + '/src/collective/foo/bar/profiles/default',
                self.project + '/src/collective/foo/bar/profiles/default/browserlayer.xml',  # noqa
                self.project + '/src/collective/foo/bar/profiles/default/metadata.xml',  # noqa
                self.project + '/src/collective/foo/bar/profiles/default/registry.xml',  # noqa
                self.project + '/src/collective/foo/bar/profiles/uninstall',
                self.project + '/src/collective/foo/bar/profiles/uninstall/browserlayer.xml',  # noqa
                self.project + '/src/collective/foo/bar/setuphandlers.py',
                self.project + '/src/collective/foo/bar/testing.py',
                self.project + '/src/collective/foo/bar/tests',
                self.project + '/src/collective/foo/bar/tests/__init__.py',
                self.project + '/src/collective/foo/bar/tests/robot',
                self.project + '/src/collective/foo/bar/tests/robot/test_example.robot',  # noqa
                self.project + '/src/collective/foo/bar/tests/test_robot.py',
                self.project + '/src/collective/foo/bar/tests/test_setup.py',
            ]
        )

    def test_plone_theme_package_template(self):
        """Test the `plone_theme_package` template.

        Generate a project from a template, test which files were created
        and run all tests in the generated package.
        """
        self.template = 'plone_theme_package'
        self.project = 'collective.foo'
        self.answers_file = 'nosetests_answers_plone_theme_package.ini'
        self.maxDiff = None
        prefix = self.project
        result = self.create_template()
        # from pprint import pprint as pp
        # pp(result.files_created.keys())
        self.assertItemsEqual(
            result.files_created.keys(),
            [
                prefix + '',  # noqa
                prefix + '/.coveragerc',  # noqa
                prefix + '/.editorconfig',  # noqa
                prefix + '/.gitattributes',  # noqa
                prefix + '/.gitignore',  # noqa
                prefix + '/.travis.yml',  # noqa
                prefix + '/bootstrap-buildout.py',  # noqa
                prefix + '/buildout.cfg',  # noqa
                prefix + '/CHANGES.rst',  # noqa
                prefix + '/CONTRIBUTORS.rst',  # noqa
                prefix + '/docs',  # noqa
                prefix + '/docs/index.rst',  # noqa
                prefix + '/docs/LICENSE.GPL',  # noqa
                prefix + '/docs/LICENSE.rst',  # noqa
                prefix + '/Gruntfile.js',  # noqa
                prefix + '/HOWTO_DEVELOP.rst',  # noqa
                prefix + '/LICENSE.GPL',  # noqa
                prefix + '/LICENSE.rst',  # noqa
                prefix + '/MANIFEST.in',  # noqa
                prefix + '/package.json',  # noqa
                prefix + '/README.rst',  # noqa
                prefix + '/requirements.txt',  # noqa
                prefix + '/setup.cfg',  # noqa
                prefix + '/setup.py',  # noqa
                prefix + '/src',  # noqa
                prefix + '/src/collective',  # noqa
                prefix + '/src/collective/__init__.py',  # noqa
                prefix + '/src/collective/foo',  # noqa
                prefix + '/src/collective/foo/__init__.py',  # noqa
                prefix + '/src/collective/foo/browser',  # noqa
                prefix + '/src/collective/foo/browser/__init__.py',  # noqa
                prefix + '/src/collective/foo/browser/configure.zcml',  # noqa
                prefix + '/src/collective/foo/browser/overrides',  # noqa
                prefix + '/src/collective/foo/browser/overrides/.gitkeep',  # noqa
                prefix + '/src/collective/foo/browser/static',  # noqa
                prefix + '/src/collective/foo/browser/static/.gitkeep',  # noqa
                prefix + '/src/collective/foo/configure.zcml',  # noqa
                prefix + '/src/collective/foo/interfaces.py',  # noqa
                prefix + '/src/collective/foo/locales',  # noqa
                prefix + '/src/collective/foo/locales/collective.foo.pot',  # noqa
                prefix + '/src/collective/foo/locales/update.sh',  # noqa
                prefix + '/src/collective/foo/profiles',  # noqa
                prefix + '/src/collective/foo/profiles/default',  # noqa
                prefix + '/src/collective/foo/profiles/default/browserlayer.xml',  # noqa
                prefix + '/src/collective/foo/profiles/default/metadata.xml',  # noqa
                prefix + '/src/collective/foo/profiles/default/registry.xml',  # noqa
                prefix + '/src/collective/foo/profiles/default/theme.xml',  # noqa
                prefix + '/src/collective/foo/profiles/uninstall',  # noqa
                prefix + '/src/collective/foo/profiles/uninstall/browserlayer.xml',  # noqa
                prefix + '/src/collective/foo/profiles/uninstall/theme.xml',  # noqa
                prefix + '/src/collective/foo/setuphandlers.py',  # noqa
                prefix + '/src/collective/foo/testing.py',  # noqa
                prefix + '/src/collective/foo/tests',  # noqa
                prefix + '/src/collective/foo/tests/__init__.py',  # noqa
                prefix + '/src/collective/foo/tests/robot',  # noqa
                prefix + '/src/collective/foo/tests/robot/test_example.robot',  # noqa
                prefix + '/src/collective/foo/tests/test_robot.py',  # noqa
                prefix + '/src/collective/foo/tests/test_setup.py',  # noqa
                prefix + '/src/collective/foo/theme',  # noqa
                prefix + '/src/collective/foo/theme/backend.xml',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-apple-touch-icon-114x114-precomposed.png',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-apple-touch-icon-144x144-precomposed.png',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-apple-touch-icon-57x57-precomposed.png',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-apple-touch-icon-72x72-precomposed.png',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-apple-touch-icon-precomposed.png',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-apple-touch-icon.png',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta-favicon.ico',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/accessibility.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/alerts.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/barceloneta-compiled.css',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/barceloneta-compiled.css.map',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/barceloneta.css',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/barceloneta.plone.export.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/barceloneta.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/barceloneta.plone.local.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/behaviors.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/breadcrumbs.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/buttons.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/code.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/contents.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/controlpanels.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/deco.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/discussion.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/dropzone.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/event.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/fonts.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/footer.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/forms.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/formtabbing.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/grid.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/header.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/image.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/loginform.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/main.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.borderradius.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.buttons.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.clearfix.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.forms.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.grid.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.gridframework.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.images.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.prefixes.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/mixin.tabfocus.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/modal.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/normalize.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/pagination.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/pickadate.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/plone-toolbarlogo.svg',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/portlets.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/print.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/scaffolding.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/search.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/sitemap.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/sitenav.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/sortable.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/states.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/tables.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/tablesorter.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/tags.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/thumbs.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/toc.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/tooltip.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/tree.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/type.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/variables.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/barceloneta/less/views.plone.less',  # noqa
                prefix + '/src/collective/foo/theme/HOWTO_DEVELOP.rst',  # noqa
                prefix + '/src/collective/foo/theme/index.html',  # noqa
                prefix + '/src/collective/foo/theme/less',  # noqa
                prefix + '/src/collective/foo/theme/less/custom.less',  # noqa
                prefix + '/src/collective/foo/theme/less/plone.toolbar.vars.less',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/LICENSE.txt',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Light.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Light.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Light.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Light.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-LightItalic.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-LightItalic.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-LightItalic.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-LightItalic.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Medium.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Medium.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Medium.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Medium.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-MediumItalic.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-MediumItalic.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-MediumItalic.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-MediumItalic.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Regular.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Regular.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Regular.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Regular.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Thin.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Thin.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Thin.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-Thin.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-ThinItalic.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-ThinItalic.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-ThinItalic.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/Roboto-ThinItalic.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-Light.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-Light.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-Light.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-Light.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-LightItalic.eot',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-LightItalic.svg',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-LightItalic.ttf',  # noqa
                prefix + '/src/collective/foo/theme/less/roboto/RobotoCondensed-LightItalic.woff',  # noqa
                prefix + '/src/collective/foo/theme/less/theme.less',  # noqa
                prefix + '/src/collective/foo/theme/less/theme.local.less',  # noqa
                prefix + '/src/collective/foo/theme/manifest.cfg',  # noqa
                prefix + '/src/collective/foo/theme/package.json',  # noqa
                prefix + '/src/collective/foo/theme/preview.png',  # noqa
                prefix + '/src/collective/foo/theme/rules.xml',  # noqa
                prefix + '/src/collective/foo/theme/template-overrides',  # noqa
                prefix + '/src/collective/foo/theme/template-overrides/.gitkeep',  # noqa
                prefix + '/src/collective/foo/theme/tinymce-templates',  # noqa
                prefix + '/src/collective/foo/theme/tinymce-templates/image-grid-2x2.html',  # noqa
                prefix + '/src/collective/foo/theme/views',  # noqa
                prefix + '/src/collective/foo/theme/views/slider-images.pt.example',  # noqa
            ]
        )


class DummyConfigurator(object):
    def __init__(self,
                 defaults=None,
                 bobconfig=None,
                 templateconfig=None,
                 variables=None,
                 quiet=False,
                 target_directory=None):
        self.defaults = defaults or {}
        self.bobconfig = bobconfig or {}
        self.variables = variables or {}
        self.quiet = quiet
        self.templateconfig = templateconfig or {}
        self.target_directory = target_directory


class HooksTest(unittest.TestCase):

    def setUp(self):
        target_directory = '/tmp/bobtemplates/plonetheme.tango'
        variables = {
            'author.email': 'info@example.com',
            'author.github.user': u'ExampleUser',
            'author.name': 'Example Name',
            'package.description': u'An add-on for Plone',
            'plone.is_plone5': True,
            'plone.minor_version': u'5.0',
            'plone.version': u'5.0.6',
            'year': 2017
        }
        self.configurator = DummyConfigurator(
            target_directory=target_directory, variables=variables)

    def test_to_boolean(self):
        # Initial simple test to show coverage in hooks.py.
        self.assertEqual(hooks.to_boolean(None, None, 'y'), True)

    def test_post_dexterity_type_name(self):
        """Test validation of entered dexterity type names
        """
        def hookit(value):
            return hooks.post_dexterity_type_name(None, None, value)

        with self.assertRaises(ValidationError):
            hookit('import')
        with self.assertRaises(ValidationError):
            hookit(u'süpertype')
        with self.assertRaises(ValidationError):
            hookit(u'Staff Member')
        with self.assertRaises(ValidationError):
            hookit(u'2ndComing')
        with self.assertRaises(ValidationError):
            hookit(u'Second Coming')
        with self.assertRaises(ValidationError):
            hookit(u'Staff Member')
        with self.assertRaises(ValidationError):
            hookit(u'*sterisk')
        self.assertEqual(hookit(u'Supertype'), u'Supertype')
        self.assertEqual(hookit(u'second_coming'), u'second_coming')
        self.assertEqual(hookit(u'the_2nd_coming'), u'the_2nd_coming')

    def test_post_theme_name(self):
        """ validation of entered theme name
        """
        def hookit(value):
            return hooks.post_theme_name(None, None, value)

        with self.assertRaises(ValidationError):
            hookit('foo bar !')
        with self.assertRaises(ValidationError):
            hookit(u'Glühwein')
        with self.assertRaises(ValidationError):
            hookit(u'.my-theme')
        with self.assertRaises(ValidationError):
            hookit(u'my-theme.')
        with self.assertRaises(ValidationError):
            hookit(u'my-theme; lala')
        with self.assertRaises(ValidationError):
            hookit(u'my theme-')

        self.assertEqual(hookit(u'My Theme'), u'My Theme')
        self.assertEqual(hookit(u'my-website.org'), u'my-website.org')
        self.assertEqual(
            hookit(u'Theme for example.com'), u'Theme for example.com')
        self.assertEqual(hookit(u'My_Theme'), u'My_Theme')
        self.assertEqual(
            hookit(u'My Theme - blue 666'), u'My Theme - blue 666')

    def test_prepare_render(self):
        """
        """
        def hookit(configurator):
            hooks.prepare_render(configurator)

        self.configurator.variables['theme.name'] = u'My Theme'
        hookit(self.configurator)
        self.assertTrue('package.nested' in self.configurator.variables)
        self.assertTrue('package.namespace' in self.configurator.variables)
        self.assertTrue('package.dottedname' in self.configurator.variables)
        self.assertTrue('package.uppercasename' in self.configurator.variables)
        self.assertTrue('theme.normalized_name' in self.configurator.variables)
        self.assertEqual(
            self.configurator.variables['theme.name'],
            'My Theme')
        self.assertEqual(
            self.configurator.variables['theme.normalized_name'],
            'my-theme')

        self.configurator.variables['theme.name'] = u'Blue    example.com'
        hookit(self.configurator)
        self.assertEqual(
            self.configurator.variables['theme.name'],
            'Blue    example.com')
        self.assertEqual(
            self.configurator.variables['theme.normalized_name'],
            'blue-example.com')

        self.configurator.variables['theme.name'] = u'Blue_Sky example.com'
        hookit(self.configurator)
        self.assertEqual(
            self.configurator.variables['theme.name'],
            'Blue_Sky example.com')
        self.assertEqual(
            self.configurator.variables['theme.normalized_name'],
            'blue-sky-example.com')
