*** Settings *****************************************************************

Library  Selenium2Library  timeout=10  implicit_wait=0.5

Suite Setup  Start browser
Suite Teardown  Close All Browsers


*** Variables ****************************************************************

${BROWSER}=  Firefox


*** Test Cases ***************************************************************

Scenario: Test Front Page
  Go to  http://localhost:55001/plone/
  Page should contain  Replace this template with your own theme


*** Keywords *****************************************************************

Start browser
  Open browser  http://localhost:55001/plone/  browser=${BROWSER}
