import unittest2 as unittest
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
        }
        return self.env.run(
            '%(dir)s/bin/mrbob -O %(project)s --config '
            '%(dir)s/test_answers.ini %(dir)s/bobtemplates/%(template)s'
            % options)


class PloneTemplateTest(BaseTemplateTest):
    """Tests for the `plone_addon` template."""
    template = 'plone_addon'
    project = 'collective.foo'

    def test_plone_addon_template(self):
        """Test the `plone_addon` template.

        Generate a project from a template, test which files were created
        and run all tests in the generated package.
        """
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
                self.project + '/bootstrap.py',
                self.project + '/buildout.cfg',
                self.project + '/buildout.d',
                self.project + '/buildout.d/base.cfg',
                self.project + '/buildout.d/checkouts.cfg',
                self.project + '/buildout.d/development.cfg',
                self.project + '/buildout.d/jenkins.cfg',
                self.project + '/buildout.d/sources.cfg',
                self.project + '/buildout.d/travis.cfg',
                self.project + '/buildout.d/versions.cfg',
                self.project + '/docs',
                self.project + '/docs/LICENSE.GPL',
                self.project + '/docs/LICENSE.rst',
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
                self.project + '/src/collective/foo/browser/overrides/.gitkeep',
                self.project + '/src/collective/foo/browser/static',
                self.project + '/src/collective/foo/browser/static/.gitkeep',
                self.project + '/src/collective/foo/configure.zcml',
                self.project + '/src/collective/foo/content',
                self.project + '/src/collective/foo/content/__init__.py',
                self.project + '/src/collective/foo/content/configure.zcml',
                self.project + '/src/collective/foo/interfaces.py',
                self.project + '/src/collective/foo/locales',
                self.project + '/src/collective/foo/locales/fr',
                self.project + '/src/collective/foo/locales/fr/LC_MESSAGES',
                self.project + '/src/collective/foo/locales/fr/LC_MESSAGES/collective.foo.po',
                self.project + '/src/collective/foo/locales/collective.foo.pot',
                self.project + '/src/collective/foo/locales/update.sh',
                self.project + '/src/collective/foo/profiles',
                self.project + '/src/collective/foo/profiles/default',
                self.project + '/src/collective/foo/profiles/default/browserlayer.xml',
                self.project + '/src/collective/foo/profiles/default/metadata.xml',
                self.project + '/src/collective/foo/profiles/testing',
                self.project + '/src/collective/foo/profiles/testing/metadata.xml',
                self.project + '/src/collective/foo/testing.py',
                self.project + '/src/collective/foo/testing.zcml',
                self.project + '/src/collective/foo/tests',
                self.project + '/src/collective/foo/tests/__init__.py',
                self.project + '/src/collective/foo/tests/test_setup.py',
            ]
        )
