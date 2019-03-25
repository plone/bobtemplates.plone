Changelog
=========

4.0.2 (2019-03-25)
------------------

- Fix git output in python 3.
  [pbauer]

- Change installer-tests to work in all Plone-Versions.
  [pbauer]

- Add `plone.translatable` as a commented behavior
  [erral]


4.0.1 (2019-03-11)
------------------

- Remove version conditions for addon dependencies, p43-p52 should be supported.
  [MrTango]


4.0 (2019-03-11)
----------------

- Only recommend using short names for behaviors, improve behavior docs.
  [MrTango]

- Generate the same tests for P4/5 packages.
  [MrTango]

- Add Tox setup to generated packages, to test multiple Python and Plone versions.
  [MrTango]

- Provided buildout, requirements and constraints for all Plone versions.
  [MrTango]

- Finally activate and fix new templates: view, viewlet, portlet, restapi_service.
  [MrTango]

- Refactor skeleton-tests setup, we call specific Tox envs inside the generated packages.
  [MrTango]

- Add Sphinx doc config to addon template docs.
  [MrTango]

- Make portlet sub-template Python 3 compatible.
  [MrTango]

- Remove skeleton test for theme_barceloneta on Plone 4
  [MrTango]

- Always include plone.restapi in setup.py
  [MrTango]

- Use newest Tox and Pytest versions, to allow running test in parallel mod on local machine.
  [MrTango]

- Add custom tox2travis.py script, to generate a Travis matrix from Tox configuration.
  [MrTango]

- Fixes #350: add "python_requires" option to setup.py.
  [jensens, iham]

- Fix some confusion in setup.py classifiers and depenencies due to introduction of Plone 5.2 support.
  Introduces plone.is_plone5.2 variable.
  [jensens]

- Fix behavior template: use separate marker interface,
  register marker in the behavior zcml and adapt content to the marker, not to IDexterityContent.
  For further reference, see the plone.behavior README.rst Example 2.
  Fixes #16.
  [fredvd, jensens]

- Use behavior shortnames in FTI.
  [jensens]

- Do not add dexterity as dependency in Plone 5.x due to the fact it is already in Plone core.
  [jensens]

- Enforce base class, when supermodel is used, to have a decent marker interface
  [MrTango]

- Fix theme templates: #349, use package_directory as target now, improve testing
  [MrTango]

- Correct viewlet example code, fixes: #351
  [MrTango]

- Add missing plone.app.themingplugins to dependencies, fixes: #353
  [MrTango]


3.6.0 (2019-02-25)
------------------

- Use @implementer decorator instead of implements.
  [erral]

- Fix FTI settings if default behaviors not active, #352
  [MrTango]

- Correct the sentence formation.
  [Akshjain99]


3.6.0b1 (2018-12-28)
--------------------

- Add support for Python 3.
  [pbauer]

- Replace portal_quickinstaller in tests for Plone 5.1+.
  [pbauer]

- Avoid linty issues in zcml files in updateing method for zcml files
  [MrTango]

- provide generic methods remove_unwanted_files/update_configure_zcml
  [MrTango]

- Add restapi_service sub-template
  [MrTango]


3.5.2 (2018-10-30)
------------------

- Improve content_type sub-template, to reduce linting issues on created code
  [MrTango]

- Replace python-slugify by custom slugify method, fixes #335 and #337
  [MrTango]

- Added safe_unicode/safe_encode and safe_nativestring methods in utils
  [MrTango]

- Add docs for view, viewlet and portlet
  [kakshay21]


3.5.1 (2018-10-23)
------------------

- Refactor and fix docs
  [MrTango]

- Fix updating of parent FTI file, when parent type name contains spaces, fixes #331
  [MrTango]

- Don't do git auto commit if git init was disabled in addon template, fixes #300
  [MrTango]


3.5.0 (2018-10-17)
------------------

- Add a new subtemplate for addon that creates a full barceloneta-based theme
  [erral]


3.4.3 (2018-10-17)
------------------

- Add a build step to report coverage on gitlab and run tests on stages
  [erral]

- Rename Roboto font files copies from barceloneta.theme to match CSS registrations
  [erral]

- Refresh backend.xml from latest plonetheme.barceloneta version so that the diazo theme resources
  are not copied into the backend.xml but dropped beforehand. Also removes toggle nav button which
  was removed from barceloneta theme. fixes #317
  [fredvd]

- Deactivated the dublicated template file definition in view Python class
  [MrTango]

- Don't override constructor in views by default
  [MrTango]

- Use --ignore-submodules in git_clean_state_check
  [MrTango]

- Commented out the HEAD SCRIPT rule in backend.xml that caused the scripts being pulled twice,
  in case that you are using it to style backend views. You should only use
  this rule once in your ruleset. Using it twice cause leads to JS errors and
  patterns initialition failures.
  This fixes: https://github.com/plone/plonetheme.barceloneta/issues/158
  [sneridagh]

- Updated "theme" subtemplate backend/frontend rules and add usage hints
  [MrTango]

- set correct classifiers for Plone 4 addons, fixes: #303
  [MrTango]

- remove boostrap-buildout.py references in config files, fixes #302
  [MrTango]

- Make adding default behaviors optional in content_type subtemplate, fixes #324
  [MrTango]

- Add deprecated flag and info to theme_package template in registry
  [MrTango]


3.4.2 (2018-08-13)
------------------

- Add portlet subtemplate
  [kakshay21]

- Replace stringcase library by case_conversion
  [kakshay21]

3.4.1 (2018-07-23)
------------------

- Fix #313 and improve tests
  [MrTango]

3.4.0 (2018-07-23)
------------------

- Add viewlet subtemplate
  [kakshay21]

- Add view subtemplate
  [kakshay21]

- Add update_locale script in bin/ folder to update locales
  [kakshay21]

- Add a custom to_boolean jinja filter
  [kakshay21]

- Add plone-compile-resources script in addon and extending .gitignore file
  [kakshay21]

- Add conditional tests in content_type
  [kakshay21]

- Improve DX CT name normalization and question info, added more tests for DX CT normalization
  [MrTango]

- Cleanup addon template, add one more test for to_boolean method
  [MrTango]


3.3.0 (2018-05-24)
------------------

- Ask for parent content_type when global_allow is set to false
  [kakshay21]

- Hide container filter options in FTI settings when dexterity_type_base_class is 'Item'
  [kakshay21]

- add package_folder_rel_path variable and fix robot test header
  [MrTango]


3.2.0 (2018-04-25)
------------------

- improve messages after using vocabulary/behavior sub-templates with names of the vocabulary or behavior
  [MrTango]

- fix behavior name registration
  [MrTango]

- Add gitlab CI config to addon template
  [MrTango]


3.2.0b3 (2018-04-20)
--------------------

- Add new field in behavior, improve test naming and tests
  [MrTango]

- Add a chapter howto upgrade existing packages to be compatible with plonecli and new bobtemplates.plone templates
  [MrTango]

- improve test naming of content_Type and vocabulary templates
  [MrTango]


3.2.0b2 (2018-04-11)
--------------------

- Fix reading default config parameters and improve git-support docs
  [MrTango]


3.2.0b1 (2018-04-11)
--------------------

- Add GIT support with clean state check and auto commit/init
  [MrTango]

- Refacture template structure and increase package test covarage
  [MrTango]


3.1.2 (2018-04-06)
------------------

- Set i18n:domain in supermodel xml files to the package domain
  [MrTango]


3.1.1 (2018-04-03)
------------------

- Fix add_view_expr in content_type template
  [MrTango]

- Fix robot test selector in content_type template
  [MrTango]

- Bump default Plone buildout version to 5.1
  [MrTango]


3.1.0 (2018-04-02)
------------------

- Add global_allow and filter_content_types questions
  [MrTango]
- don't use lower case version for CT name
  [MrTango]
- add behavior tests
  [MrTango]

3.0.1 (2018-03-29)
------------------

- Use set return-status-codes=True for tox, fixes #261
  [MrTango]

- set filter_content_types to False by default, fixes #256
  [MrTango]

- add ILeadImage behavior to FTI list of inactive behaviors, fixes #255
  [MrTango]


3.0.0 (2018-03-28)
------------------

- make final release of version 3


3.0.0b5 (2018-03-27)
--------------------

- enable lockingbehavior by default and reenable locking condition for edit button, fixes #257
  [MrTango]

- only require plone.app.dexterity<=2.1.1 and not excact that version for Plone 4
  [MrTango]


3.0.0b4 (2018-03-26)
--------------------

- Use more specific names for generated test files, like test_vocab_todo_tasks.py instead of test_todo_tasks.py
  [MrTango]


3.0.0b3 (2018-03-22)
--------------------

- Add behavior sub-template entrypoint, to make it available in plonecli
  [MrTango]
- Update link to document in README.
  [kakshay21]


3.0.0b2 (2018-02-27)
--------------------

- fixed FTI configuration, removed the plone_lock_info condition
  [MrTango]


3.0.0b1 (2018-02-25)
--------------------

- Quote version strings in YAML. See: https://github.com/travis-ci/docs-travis-ci-com/issues/1540
  [thet]

- Use default Travis notifications.
  Until now only the creator of the package would get a notification, instead of the committer.
  Fixes `issue 208 <https://github.com/plone/bobtemplates.plone/issues/208>`_.
  [maurits]

- Fixed the pypi index to explicitly reference https://pypi.python.org/simple/ to prevent buildout from defaulting to the old and unsupported http:// url.
  [pigeonflight]

- Fix coveralls for packages created with addon and theme_package by converting the pickle output of createcoverage in .coverage to json.
  [pbauer]

- Fixes #235: Different roles in tests for install and uninstall.
  Use Manager role in uninstall test.
  Then both install and uninstall are executed with role Manager.
  [jensens]

- fix linting problems and error in theme_package tests
  [MrTango]

- Update setuptools and zc.buildout versions.
  [tmassman]

- Improve docs by fixing some reST, typos and grammar
  [svx]

- Update link to docs.plone.org in README
  [svx]

- Imporve docs template for valid reST generation
  [svx]

- use bobtemplate.cfg to store meta data for sub-templates #245
  [MrTango]

- fix naming of vocabularies
  [MrTango]

- fix buildout template and add some docs about the used buildout.plonetest configuration
  [MrTango]

- add behavior sub-template to create Plone behaviors
  [MrTango]


3.0.0a3 (2017-10-30)
--------------------

- Fix #222 default travis setup is broken.
  [jensens, pbauer]

- Add template registration for mr.bob/plonecli for all provided templates
  [MrTango]

- Fix content_type and theme sub templates
  [MrTango]

- fix in themes.rst changed plone_addon to addon
  [pigeonflight]


3.0.0a2 (2017-10-01)
--------------------

- Cleanup Package - remove unnecessary files from past versions
  [loechel]

- Add vocabulary subtemplate
  [MrTango]


3.0.0a1 (2017-09-26)
--------------------

- Refacturing to support subtemplates
  [MrTango]

- Add theme and content_type subtemplates
  [MrTango]

- Add missing plone namespace, to avoid conflicts with other bobtemplate packages
  [MrTango]

- Removed bootstrap-buildout.py, Update barceloneta less files for theme_package
  [agitator]

- Fixed i18n attributes for View/Edit actions in dexterity type xml.
  [maurits]

- Testing of generated skeletons integrated with tox and pytest.
  [loechel]


2.0.0 (2017-08-28)
------------------

- Set the zope_i18n_compile_mo_files environment variable.
  [maurits]

- Fixed i18n attributes for View/Edit actions in dexterity type xml.
  [maurits]

- Separate theme template from addon template, we now have plone_addon and plone_theme_package
- Update barceloneta less files to 1.7.3 for plone_theme_package
  [agitator]
- Removed bootstrap-buildout.py and added DEVELOP.rst
  [agitator]

- Update barceloneta less files to 1.7.3 for plone_theme_package
  [agitator]

- Fixed i18n attributes for View/Edit actions in dexterity type xml.  [maurits]

- Seperate theme template from addon template, we now have plone_addon and plone_theme_package
  [MrTango]

- Update pins in the generated buildout.cfg
  [ale-rt]

- Change default values for code analysis' ``return-status-codes`` directive:
  it is now ``False`` on development and ``True`` on CI.
  [hvelarde]

- Pin flake8 to latest (3.3.0) to allow use of latest pycodestyle (2.3.1)
  [fulv]

- Imrove wording
  [svx]

- Add requirements.txt and update README.txt to use it
  [MrTango]

- Make cleanup hook windows friendly.
  [gforcada]

- Move LICENSE.rst out of docs folder into top level.
  [gforcada]

- Get rid of the last two code violations on generated package
  [sneridagh]

- Comment the toolbar rule by default in backend.xml and add a comment on how
  to add it properly if backend.xml is used. Declaring the toolbar rule twice
  causes the toolbar JS stop working properly
  [sneridagh]


1.0.5 (2016-10-16)
------------------

- Use same lines width than package name for title ##
  [AuroreMariscal]

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
