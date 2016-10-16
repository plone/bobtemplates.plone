Changelog
=========

1.0.5 (2016-10-16)
------------------

- Get rid of ``travis.cfg`` configuration as its use is no longer considered best practice.
  [hvelarde]

- Update ``bootstrap-buildout.py`` to latest version.
  [hvelarde]

- Fix imports to follow conventions.
  [hvelarde]

- Avoid usage of double quotes on strings.
  [hvelarde]

- Avoid usage of invokeFactory.
  [hvelarde]

- Remove dependency on unittest2 as package is not intended to be compatible with Python 2.6.
  [hvelarde]

- Use selenium v2.53.6.
  [hvelarde]

- Use plone:static instead of browser:resourceDirectory to allow ttw-overrrides.
  [pbauer]

- Bump flake8 version to 3.x.
  [gforcada]

- Update theme template, include complete working Barceloneta resources + grunt setup
  [MrTango]


1.0.4 (2016-07-23)
------------------

- Upgrade some pinns.
  [pbauer]

- Upgrade to 5.0.5 and test against that.
  [pbauer]

- Add ``i18n:attributes`` for action nodes in FTI profile.
  [thet]

- Pin versions of coverage/createcoverage
  [staeff]

- Default to Plone 5.0.4.
  [jensens]

- Validate type name input (fixes #81).
  [pbauer]

- Git ignore ``.installed.cfg`` and ``mr.developer.cfg`` by default.
  [jensens]

- ``isort`` style checks are enabled, but no config was set. i
  Added config according to http://docs.plone.org/develop/styleguide/python.html#grouping-and-sorting
  [jensens]

- Ordered sections of generated FTI xml into semantical block and added comments for each block.
  [jensens]

- Bump setuptools version to 21.0.0 in buildout.cfg.bob
  [staeff]

- Configure buildout to install all recommended codeanalysis plugins
  [staeff]


1.0.3 (2016-04-13)
------------------

- Fix Plone default version (Plone 4.3.9).
  [timo]


1.0.2 (2016-04-13)
------------------

- Create uninstall profile also for Plone 4.3.x, since it already depends on ``Products.CMFQuickInstallerTool >= 3.0.9``.
  [thet]

- Update Plone versions to 4.3.9 and 5.0.4.
  [thet]

- Update robot test framework versions including Selenium to work with recent firefox releases.
  [thet]

- Replaced import steps by post_handlers.  Needs GenericSetup 1.8.2 or
  higher.  This is included by default in Plone 4.3.8 and 5.0.3 but
  should be fine to use on older Plone versions.  [maurits]

- Removed ``.*`` from the ``.gitignore`` file.  This would ignore the
  ``.gitkeep`` files, which would mean some directories are not added
  when you do ``git add`` after generating a new project.  [maurits]

- Note about disabled ``z3c.autoinclude`` in test layer setup.
  [thet]

- Remove the ``xmlns:five`` namespace, as it is not used at all.
  [thet]

- Fix build failure on Plone 4.x due to plone.app.contenttypes pulled in and having a plone.app.locales >= 4.3.9 dependency in it's depending packages.
  [thet]

- Declare the xml encoding for all GenericSetup profile files.
  Otherwise the parser has to autodetect it.
  Also add an xml version and encoding declaration to ``theme.xml``.
  [thet]

- Add "(uninstall)" to the uninstall profile title.
  Otherwise it cannot be distinguished from the install profile in portal_setup.
  [thet]

- Simplify concatenation of ``.rst`` files for ``setup.py``.
  [thet]

- Update ``.gitignores`` in repository to exclude ``lib64``, ``pip-selfcheck.json`` and all ``.*`` except necessary.
  Update ``.gitignore.bob`` in templates with these changes too.
  Add ``.gitattributes`` in repository for union-merge CHANGES.rst files.
  [thet]

- Update docs and README
  [svx]

1.0.1 (2015-12-12)
------------------

- Register locales directory before loading dependencies to avoid issues when overriding translations.
  [hvelarde]


1.0 (2015-10-02)
----------------

- Upgrade to Plone 4.3.7 and 5.0.
  [timo]

- Avoid pyflakes warnings for long package names.
  [maurits]


1.0b1 (2015-09-17)
------------------

- Always start with 1.0a1. No more 0.x releases please.
  [timo]

- Use Plone minor version for ``setup.py`` classifier. So 4.3 instead
  of 4.3.6.
  [maurits]

- Enabled robot part in generated package.
  [maurits]

- Add depedency on plone.testing 5.0.0. Despite the major version number,
  this change does not contain breaking changes.
  [do3cc]

- Fix #84 Make travis cache the egg directory of the generated package.
  [jensens]

- Update tests to use Plone 5.0b3.
  [jensens]

- Remove unittest2 dependency.
  [gforcada]


0.11 (2015-07-24)
-----------------

- Fix update.sh
  [pbauer]

- Add i18ndude to buildout
  [pbauer]

- Fix package-creation on Windows. Fixes #72.
  [pbauer]

- Add packagename to licence.
  [pbauer]

- Add uninstall-profile for Plone 5.
  [pbauer]

- Fix indentation to follow the conventions of plone.api.
  [pbauer]

- Move badges from pypin to shields.io.
  [timo]

- Fix coverage on travis template.
  [gil-cano]

- Enable code analysis on travis and fail if the code does not pass.
  [gforcada]


0.10 (2015-06-15)
-----------------

- Add check-readme script that detects Restructured Text issues.
  [timo]

- Use only version up to minor version in setup.py of package #56.
  [tomgross]

- Use class method to load ZCML in tests.
  [tomgross]

- Upgrade default Plone version to 4.3.6.
  [timo]

- Add zest.releaser to package buildout.
  [timo]

- Update README according to Plone docs best practice.
  [do3cc, timo]

- Add flake8-extensions to code-analysis.
  [timo]

- Upgrade Selenium to 2.46.0.
  [timo, pbauer]

- Don't create a type-schema unless it is needed.
  [pbauer]


0.9 (2015-03-24)
----------------

- Add Theme package type with simple bootstrap-based theme.
  [timo]

- Add Dexterity package type.
  [timo]

- Remove example view.
  [timo]

- Remove question for keywords.
  [timo]

- Remove question for locales.
  [timo]

- Remove questions for version and license.
  [timo]

- Remove questions for profile, setuphandler, and testing.
  [timo]

- Unify buildout configuration in buildout.cfg
  [timo]

- Fix bootstrap command in travis.yml.
  [timo]


0.8 (2015-02-06)
----------------

- Add includeDependencies. This fixes #23.
  [timo]


0.7 (2015-02-05)
----------------

- Use latest buildout-bootstrap.py.
  [timo]

- Fix failing nosetests.
  [timo]

- Add test that creates an add_on and runs all its tests and code analysis.
  [timo]

- Run tests on travis.
  [timo]

- Run code analysis on travis. Build fails on PEP8 violations.
  [timo]

- Add code analysis.
  [timo]

- Remove z2.InstallProducts. Not needed any longer.
  [timo]

- Use testing best practices and follow common naming conventions.
  [timo]

- Remove testing profile. Global testing state is considered an anti-pattern.
  [timo]

- Add example robot test.
  [timo]

- Add travis and pypip.in badges.
  [timo]

- Run code analysis on the generated addon as well within the tests to make
  sure we always ship 100% PEP8 compliant code.
  [timo]

- Add REMOTE_LIBRARY_BUNDLE_FIXTURE to acceptance test fixture.
  [timo]


0.6 (2015-01-17)
----------------

- Use PLONE_APP_CONTENTTYPES_FIXTURE for tests on when using Plone 5.
  [pbauer]


0.5 (2015-01-17)
----------------

- Remove useless base-classes for tests. Use 'layer = xxx' instead.
  [pbauer]

- Fix some minor code-analysis issues.
  [pbauer]

- Added .editorconfig file.
  [ale-rt]


0.4 (2014-12-08)
----------------

- Remove grok.
  [pbauer]

- Fix missed removals when testing was deselected.
  [pbauer]

- Only use jbot when there is a profile and a browser layer.
  [pbauer]

- Get username and email from git.
  [do3cc]


0.3 (2014-12-07)
----------------

- Pinn robotframework to 2.8.4 to fix package-tests.
  [pbauer]

- Add browserlayer to demoview to allow multiple addons.
  [pbauer]

- Fix creation of nested packages (wrong __init__.py).
  [pbauer]


0.2 (2014-12-07)
----------------

- Fix documentation
  [pbauer]


0.1 (2014-12-07)
----------------

- Get namespace, name and type from target-dir.
  [pbauer]

- Remove obsolete plone_addon_nested. Auto-nest package in after-render hook.
  [pbauer]

- Add many new features. Most of them are optional.
  [pbauer]

- Initial import based on bobtemplates.ecreall by
  cedricmessiant, vincentfretin and thomasdesvenain.
  [pbauer]
