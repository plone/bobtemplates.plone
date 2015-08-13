#!/bin/sh
# just a  template, used by buildout to generate a test script to run tests
# of the addon
set -e

# use mr.bob
${buildout:directory}/bin/mrbob -O ${:addon_name} bobtemplates:plone_addon --config test_answers.ini

# buildout addon
cd ${buildout:directory}/${:addon_name}
virtualenv ${buildout:directory}/${:addon_name}
${buildout:directory}/${:addon_name}/bin/python bootstrap-buildout.py --setuptools-version=8.3
${buildout:directory}/${:addon_name}/bin/buildout

# run tests on addon
${buildout:directory}/${:addon_name}/bin/test --all
${buildout:directory}/${:addon_name}/bin/code-analysis

# remove addon
rm -rf ${buildout:directory}/${:addon_name}/
