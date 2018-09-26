from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import uuid
from tempest import config
import logging

logger = logging.getLogger(__name__)
CONF = config.CONF
browser = None


def get_browser():
    global browser
    if browser is not None:
        return browser

    # open the default conf file (default.conf.json points to the
    # default conf file which will be opened)
    browser_driver = None
    try:
        browser_driver = CONF.tripleo_ui.webdriver
    except Exception as e:
        logger.error(e)
        return None

    if browser_driver.lower() == 'firefox':
        browser_factory = FirefoxFactory()
    elif browser_driver.lower() == "marionette":
        browser_factory = MarionetteFactory(
            CONF.tripleo_ui.marionette_binary)
    elif browser_driver.lower() == "chrome":
        browser_factory = ChromeFactory()
    else:
        logger.warning("configured browser '{}' is unknown, using "
                       "Firefox as default".format(browser_driver))
        browser_factory = FirefoxFactory()

    browser = Browser(browser_factory, CONF.tripleo_ui.url)
    return browser


def quit_browser():
    global browser
    if browser is None:
        return

    browser.quit_browser()
    browser = None


def save_screenshot(filename=None):
    global browser
    if browser is None:
        return

    if not filename:
        filename = "/tmp/{}.png".format(uuid.uuid4())
    browser.get_driver().save_screenshot(filename)
#     logger.log("Snapped screenshot: {}".format(filename))
    return filename


def execute_script(script_to_run):
    return get_browser().execute_script(script_to_run)


class Browser(object):

    def __init__(self, browser_factory, homepage=None):
        self.driver = browser_factory.create()
        if homepage and len(homepage.strip()):
            self.get(homepage)

    def get(self, url):
#         logger.assertion(self.driver,
#                          "browser was already closed",
#                          take_screenshot=False)
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def get_driver(self):
        return self.driver

    def quit_browser(self):
#         logger.assertion(self.driver,
#                          "browser was already closed",
#                          take_screenshot=False)
        self.driver.quit()
        self.driver = None

    def execute_script(self, script_to_run):
        return self.driver.execute_script(script_to_run)


class BrowserFactory(object):
    pass


class FirefoxFactory(BrowserFactory):

    def create(self):
        return webdriver.Firefox()


class ChromeFactory(BrowserFactory):

    def create(self):
        return webdriver.Chrome()


class MarionetteFactory(BrowserFactory):

    def __init__(self, path_to_binary):
#         logger.assertion(path_to_binary and len(path_to_binary),
#                          "path to marionette executable is mandatory",
#                          take_screenshot=False)
        self.path_to_binary = path_to_binary

    def create(self):
        capabilities = DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True
        args = dict()
        args['capabilities'] = capabilities
        args['executable_path'] = self.path_to_binary
        return webdriver.Firefox(**args)

