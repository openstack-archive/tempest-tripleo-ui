from tempest_tripleo_ui.core import SeleniumElement


username = SeleniumElement.byId("username")
password = SeleniumElement.byId("password")
logoutButton = SeleniumElement.byId('NavBar__logoutLink')
userToggleButton = SeleniumElement.byId('UserDropdown__toggle')

unauthorizedDiv = SeleniumElement.byXpath(
    '//div[contains(@class, "login")]/div[contains'
    '(@class, "alert-danger")]')
modalDiv = SeleniumElement.byXpath(
    '//div[contains(@class, "modal")][contains(@role, "dialog")]')
