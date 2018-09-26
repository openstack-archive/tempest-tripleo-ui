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

    browser_driver = CONF.tripleo_ui.webdriver.lower()
    if browser_driver == "chrome":
        browser_factory = ChromeFactory()
    if browser_driver == "firefox":
        browser_factory = MarionetteFactory(
            CONF.tripleo_ui.marionette_binary)
    # FIXME: fail if browser_driver is set wrong in the conf file 

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
    return filename


def execute_script(script_to_run):
    return get_browser().execute_script(script_to_run)


class Browser(object):

    def __init__(self, browser_factory, homepage=None):
        self.driver = browser_factory.create()
        if homepage and len(homepage.strip()):
            self.get(homepage)

    def get(self, url):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def get_driver(self):
        return self.driver

    def quit_browser(self):
        self.driver.quit()
        self.driver = None

    def execute_script(self, script_to_run):
        return self.driver.execute_script(script_to_run)


class ChromeFactory(object):

    def create(self):
        return webdriver.Chrome()


class MarionetteFactory(object):

    def __init__(self, path_to_binary):
        self.path_to_binary = path_to_binary

    def create(self):
        capabilities = DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True
        args = dict()
        args['capabilities'] = capabilities
        args['executable_path'] = self.path_to_binary
        return webdriver.Firefox(**args)
