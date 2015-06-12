import unittest
import os
import tempfile
import shutil

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
    """Tests for the `plone_addon` template."""
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
                self.project + '/.gitignore',
                self.project + '/.travis.yml',
                self.project + '/CHANGES.rst',
                self.project + '/CONTRIBUTORS.rst',
                self.project + '/MANIFEST.in',
                self.project + '/README.rst',
                self.project + '/bootstrap-buildout.py',
                self.project + '/buildout.cfg',
                self.project + '/docs',
                self.project + '/docs/LICENSE.GPL',
                self.project + '/docs/LICENSE.rst',
                self.project + '/docs/index.rst',
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
                self.project + '/src/collective/foo/profiles/default/collectivefoo_marker.txt',  # noqa
                self.project + '/src/collective/foo/profiles/default/metadata.xml',  # noqa
                self.project + '/src/collective/foo/setuphandlers.py',
                self.project + '/src/collective/foo/testing.py',
                self.project + '/src/collective/foo/tests',
                self.project + '/src/collective/foo/tests/__init__.py',
                self.project + '/src/collective/foo/tests/robot',
                self.project + '/src/collective/foo/tests/robot/test_example.robot',  # noqa
                self.project + '/src/collective/foo/tests/test_robot.py',
                self.project + '/src/collective/foo/tests/test_setup.py',
                self.project + '/travis.cfg',
                self.project + '/.coveragerc',
                self.project + '/.editorconfig',
                self.project + '/.gitattributes',
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
                self.project + '/.gitignore',
                self.project + '/.travis.yml',
                self.project + '/CHANGES.rst',
                self.project + '/CONTRIBUTORS.rst',
                self.project + '/MANIFEST.in',
                self.project + '/README.rst',
                self.project + '/bootstrap-buildout.py',
                self.project + '/buildout.cfg',
                self.project + '/docs',
                self.project + '/docs/LICENSE.GPL',
                self.project + '/docs/LICENSE.rst',
                self.project + '/docs/index.rst',
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
                self.project + '/src/collective/foo/bar/profiles/default/collectivefoobar_marker.txt',  # noqa
                self.project + '/src/collective/foo/bar/profiles/default/metadata.xml',  # noqa
                self.project + '/src/collective/foo/bar/setuphandlers.py',
                self.project + '/src/collective/foo/bar/testing.py',
                self.project + '/src/collective/foo/bar/tests',
                self.project + '/src/collective/foo/bar/tests/__init__.py',
                self.project + '/src/collective/foo/bar/tests/robot',
                self.project + '/src/collective/foo/bar/tests/robot/test_example.robot',  # noqa
                self.project + '/src/collective/foo/bar/tests/test_robot.py',
                self.project + '/src/collective/foo/bar/tests/test_setup.py',
                self.project + '/travis.cfg',
                self.project + '/.coveragerc',
                self.project + '/.editorconfig',
                self.project + '/.gitattributes',
            ]
        )
