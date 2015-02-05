*** Settings *****************************************************************

Library  Selenium2Library  timeout=10  implicit_wait=0.5

Suite Setup  Start browser
Suite Teardown  Close All Browsers


*** Variables ****************************************************************

${BROWSER}=  Firefox
${PLONE_URL}=  http://localhost:55001/plone/

*** Test Cases ***************************************************************

Scenario: Test Front Page
  Go to  ${PLONE_URL}
  Page should contain  Plone site


*** Keywords *****************************************************************

Start browser
  Open browser  ${PLONE_URL}  browser=${BROWSER}
