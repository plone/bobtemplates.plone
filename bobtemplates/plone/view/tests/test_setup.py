def test_custom_template(self):
    setRoles(self.portal, TEST_USER_ID, ['Manager'])
    self.portal.invokeFactory(
            "talk",
            id="my-talk",
            title="My Talk",
        )

    import transaction
    transaction.commit()

    self.browser.open(self.portal_url + '/myview')

    self.assertIn('Magic templates in Plone 5', self.browser.contents)
    self.assertIn('The State of Plone', self.browser.contents)
    