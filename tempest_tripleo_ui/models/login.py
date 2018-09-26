from tempest_tripleo_ui.widgets import login_page
from tempest_tripleo_ui import alerts
from tempest_tripleo_ui.timer import Timer
from time import sleep
from tempest import config
import logging

CONF = config.CONF
logger = logging.getLogger(__name__)


def logout():
    logger.info("Logging out...")
    if not is_logged_in():
        logger.warning("Hey! Was already logged out...")
        return

    while alerts.clearDangerMessage(timeout=1) or \
            alerts.clearSuccessMessage(timeout=1):
        pass

    # First, we need to click on the toggle to open the user dropdown menu
    if login_page.userToggleButton.waitForElement(0):
        if not login_page.userToggleButton.click():
            logger.error("click failed on the 'user toggle' button")

    if not login_page.logoutButton.click():
        logger.error("click failed on the 'Logout' button")
    # FIXME: get this assertion to work
    # logger.assertion(
    #     login_page.password.waitForElement(5),
    #     "Logout failed (didn't see the login screen after 5 seconds)")
    return True


def is_logged_in():
    for _retries in range(0, 5):
        # find the logout button or the password field,
        # whichever comes first
        if login_page.logoutButton.waitForElement(1):
            return True

        if login_page.password.waitForElement(1):
            return False

    logger.error("login.is_logged_in(): could not determine if "
                 "logged in or not, no recognizable elements found "
                 "on the page within 10 seconds")
    return False


def login(username=None, password=None):
    logger.info("Logging in...")
    if is_logged_in():
        logger.error("Already logged in... Make sure "
                     "you log out first!")
        return False

    if username is None:
        username = CONF.auth.admin_username
    if password is None:
        password = CONF.auth.admin_password
    if username is None or password is None:
        logger.error("Missing username or password. Make sure they are "
                     "configured in the tempest conf file")
        return False

    login_page.username.clear()
    login_page.username.send_keys(username)
    login_page.password.clear()
    login_page.password.send_keys(password)
    login_page.password.submit()

    timeout = 60

    if not login_page.logoutButton.waitForElement(timeout):
        if login_page.unauthorizedDiv.waitForElement(1) is not None:
            logger.warning(login_page.unauthorizedDiv.getAllText())
            return False

        logger.error(
            "Login failed (waited {} seconds and no sign of "
            "a logout button...)".format(timeout))
        return False

    # wait for the modal div that covers the page to go away...
    timeout = 20
    timer = Timer("wait for modal after login", timeout=timeout)
    while login_page.modalDiv.waitForElement(1) and \
            timer.getDuration() < timeout:
        sleep(1)

    if not timer.assert_timer():
        logger.error("exceeded timer")
        return False
    if timer.getDuration() > 5:
        logger.warning("login took {} seconds".format(
            timer.getDuration()))

    # wait for all spinners
    alerts.waitForSpinner()

    # clear all alerts that sometimes appear straight after login
    while alerts.clearDangerMessage():
        pass

    return True
