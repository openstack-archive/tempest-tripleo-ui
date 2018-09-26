from tempest_tripleo_ui.core import SeleniumElement


username = SeleniumElement.by_id("username")
password = SeleniumElement.by_id("password")
logout_button = SeleniumElement.by_id('NavBar__logoutLink')
user_toggle_button = SeleniumElement.by_id('UserDropdown__toggle')

unauthorized_div = SeleniumElement.by_xpath(
    '//div[contains(@class, "login")]/div[contains'
    '(@class, "alert-danger")]')
modal_div = SeleniumElement.by_xpath(
    '//div[contains(@class, "modal")][contains(@role, "dialog")]')
