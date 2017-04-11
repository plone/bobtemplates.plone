#!/bin/sh
# just a  template, used by buildout to generate a test script to run tests
# of the addon
set -e

# use mr.bob
${buildout:directory}/bin/mrbob -O ${:addon_name} -n bobtemplates:plone_addon --config test_answers.ini

# buildout addon
cd ${buildout:directory}/${:addon_name}
virtualenv ${buildout:directory}/${:addon_name}
${buildout:directory}/${:addon_name}/bin/python bootstrap-buildout.py --setuptools-version=8.3
${buildout:directory}/${:addon_name}/bin/buildout code-analysis:return-status-codes=True

# run tests on addon
${buildout:directory}/${:addon_name}/bin/test --all
# save the exit code of the test command
testresult=$?

# run code analysis
${buildout:directory}/${:addon_name}/bin/code-analysis

# remove addon
rm -rf ${buildout:directory}/${:addon_name}/

# return the exit code of the test command
exit $testresult
