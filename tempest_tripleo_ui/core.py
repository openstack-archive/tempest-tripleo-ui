from tempest_tripleo_ui.services import browser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from tempest_tripleo_ui.decorators import selenium_action
import logging

logger = logging.getLogger(__name__)


class Identifier(object):
    def __init__(self, by, identifier):
        self.by = by
        self.identifier = identifier

    @classmethod
    def Xpath(cls, locator):
        return Identifier(By.XPATH, locator)

    @classmethod
    def CssSelector(cls, locator):
        return Identifier(By.CSS_SELECTOR, locator)

    @classmethod
    def Id(cls, locator):
        return Identifier(By.ID, locator)

    @classmethod
    def ClassName(cls, locator):
        return Identifier(By.CLASS_NAME, locator)

    @classmethod
    def LinkText(cls, locator):
        return Identifier(By.LINK_TEXT, locator)


class SeleniumElement(object):

    def __init__(self,
                 identifier=None,
                 webelement=None,
                 browser=None):
        self.identifier = identifier
        self._browser = browser
        self.webelement = webelement

    @classmethod
    def byId(cls, name, browser=None):
        return SeleniumElement(Identifier(By.ID, name),
                               browser=browser)

    @classmethod
    def byClass(cls, name, browser=None):
        return SeleniumElement(Identifier(By.CLASS_NAME, name),
                               browser=browser)

    @classmethod
    def byCss(cls, name, browser=None):
        return SeleniumElement(Identifier(By.CSS_SELECTOR, name),
                               browser=browser)

    @classmethod
    def byXpath(cls, name, browser=None):
        return SeleniumElement(Identifier(By.XPATH, name),
                               browser=browser)

    @classmethod
    def byLinkText(cls, name, browser=None):
        return SeleniumElement(Identifier(By.LINK_TEXT, name),
                               browser=browser)

    def getElement(self):
        if self.webelement:
            return self.webelement

        elem = self.waitForElement()
        if elem is None:
            logger.error("can't find element: {}".format(self.get_name()))

        return elem

    def get_name(self):
        name = "No identifier"
        if self.identifier:
            name = self.identifier.identifier
        return name

    def waitForElement(self, timeout_in_seconds=10):
        if self.identifier is None:
            logger.warning("waitForElement() is irrelevant for elements "
                           "that were not found via an identifier")
            return self.webelement

        try:
            self.webelement = WebDriverWait(
                self.getBrowser().get_driver(),
                timeout_in_seconds).until(
                    EC.presence_of_element_located(
                        (self.identifier.by, self.identifier.identifier))
            )

            return self.webelement
        except BaseException:
            return None

    def waitForPresentText(self, text, timeout_in_seconds=10):
        try:
            if self.identifier is None:
                logger.warningrning(
                    'waitForPresentText will not work properly, '
                    'because there is missing .identifier.')
            self.webelement = WebDriverWait(
                self.getBrowser().get_driver(),
                timeout_in_seconds).until(
                EC.text_to_be_present_in_element(
                    (self.identifier.by, self.identifier.identifier), text)
            )
            return self.webelement
        except BaseException:
            return None

    def waitForStaleness(self, timeout_in_seconds=10):
        if self.webelement is None:
            logger.warning("waitForStaleness() is irrelevant for elements "
                           "that were not found yet")
            return True

        try:
            return WebDriverWait(self.getBrowser().get_driver(),
                                 timeout_in_seconds).until(
                EC.staleness_of(self.webelement))
        except BaseException:
            return False

    def isStale(self):
        try:
            self.webelement.is_enabled()
            return False
        except StaleElementReferenceException:
            return True
        except BaseException:
            return False

    def getBrowser(self):
        if self._browser:
            return self._browser
        return browser.get_browser()

    @selenium_action
    def isVisible(self, webelement):
        return webelement.is_displayed()

    @selenium_action
    def isSelected(self, webelement):
        return webelement.is_selected()

    @selenium_action
    def isEnabled(self, webelement):
        return webelement.is_enabled()

    @selenium_action
    def getTagName(self, webelement):
        return webelement.tag_name

    @selenium_action
    def getText(self, webelement):
        return webelement.text

    def getAllText(self):
        text = self.getText()
        if text is None or len(text) == 0:
            text = ""

        child_elements = self.findChildElements(Identifier.Xpath("*"))
        if child_elements is not None and len(child_elements) > 0:
            for child_element in child_elements:
                child_text = child_element.getAllText()
                if child_text is not None and len(child_text) > 0:
                    if len(text) > 0:
                        text = text + " " + child_text
                    else:
                        text = child_text
        return text

    @selenium_action
    def getId(self, webelement):
        return webelement.get_attribute("id")

    @selenium_action
    def getName(self, webelement):
        return webelement.get_attribute("name")

    @selenium_action
    def getValue(self, webelement):
        return webelement.get_attribute("value")

    @selenium_action
    def getClass(self, webelement):
        return webelement.get_attribute("class")

    @selenium_action
    def getHref(self, webelement):
        return webelement.get_attribute("href")

    @selenium_action
    def getTitle(self, webelement):
        return webelement.get_attribute("title")

    @selenium_action
    def click_minimum_retries(self, webelement):
        webelement.click()

    # this WON'T be a @selenium_action because we're handling retries
    # internally
    def click(self, use_js=False):

        # try to click and catch exception
        try:
            self.click_minimum_retries()
            return True
        except BaseException:
            pass

        sleep(1)

        # click failed - scroll the item into view (bottom) and try again
        try:
            self.scrollIntoView(False)
            self.click_minimum_retries()
            return True
        except BaseException:
            pass

        sleep(1)

        # click failed again - scroll the item into view (top) and try again
        try:
            self.scrollIntoView(True)
            self.click_minimum_retries()
            return True
        except BaseException:
            pass

        if use_js:
            try:
                logger.warning("almost giving up on all click attempts !!")
                self.getBrowser().save_screenshot()

                self.getBrowser().get_driver().execute_script(
                    'return arguments[0].click();', self.getElement()
                )

                logger.warning(
                    "click was successful only when using "
                    "javascript... {}".format(self.get_name()))
                sleep(1)
                self.getBrowser().save_screenshot()
                return True
            except BaseException:
                logger.warning(
                    "click was unsuccessful even with javascript! {}".format(
                        self.get_name()))

        # all failed...
        logger.error(
            "all click attempts failed on: {}".format(
                self.get_name()))
        return False

    @selenium_action
    def click_at_offset(self, webelement, x, y):
        actions = ActionChains(self.getBrowser().get_driver())
        actions.move_to_element_with_offset(webelement, x, y)
        actions.click()
        return actions.perform()

    @selenium_action
    def moveTo(self, webelement):
        actions = ActionChains(self.getBrowser().get_driver())
        actions.move_to_element(webelement)
        actions.perform()

    @selenium_action
    def scrollIntoView(self, webelement, align_to_top=True):
        driver = self.getBrowser().get_driver()
        if align_to_top:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", webelement)
        else:
            driver.execute_script(
                "arguments[0].scrollIntoView(false);", webelement)

    @selenium_action
    def submit(self, webelement):
        return webelement.submit()

    @selenium_action
    def clear(self, webelement):
        webelement.clear()
        return webelement.get_attribute('value') == ''

    @selenium_action
    def send_keys(self, webelement, text, tokenize=True):
        text = "{}".format(text)
        if not tokenize:
            webelement.send_keys(text)
            return

        # don't send more than 40 characters at a time, as it
        # can hang some scripts
        token_size = 40
        while len(text) > 0:
            webelement.send_keys(text[:token_size])
            text = text[token_size:]

    @selenium_action
    def send_ctrl_something(self, webelement, key):
        return webelement.send_keys(Keys.CONTROL, self.key)

    # start xpath with ".//"
    @selenium_action
    def findChildElements(self, webelement, identifier):
        elements = None
        try:
            elements = webelement.find_elements(
                by=self.identifier.by,
                value=self.identifier.identifier)
        except BaseException:
            return None

        if elements is not None:
            ret = []
            for childElement in elements:
                ret.append(SeleniumElement.byElement(childElement,
                                                     self.getBrowser()))
            return ret

    def drag_and_drop(self, target):
        if self.isVisible() and target.isVisible():
            elem_from = self.getElement()
            elem_to = target.getElement()
            if elem_from and elem_to:
                ActionChains(self.getBrowser().get_driver()).drag_and_drop(
                    elem_from, elem_to).perform()
        else:
            logger.error("drag-n-drop: items are not visible")

    @selenium_action
    def deselectAll(self, webelement):
        select = Select(webelement)
        return select.deselect_all()

    @selenium_action
    def selectByIndex(self, webelement, index):
        select = Select(webelement)
        return select.select_by_index(index)

    @selenium_action
    def selectByValue(self, webelement, value):
        select = Select(webelement)
        return select.select_by_value(value)

    @selenium_action
    def selectByVisibleText(self, webelement, value):
        select = Select(webelement)
        return select.select_by_visible_text(value)

    @selenium_action
    def deselectByIndex(self, webelement, index):
        select = Select(webelement)
        return select.deselect_by_index(index)

    @selenium_action
    def deselectByValue(self, webelement, value):
        select = Select(webelement)
        return select.deselect_by_value(value)

    @selenium_action
    def deselectByVisibleText(self, webelement, value):
        select = Select(webelement)
        return select.deselect_by_visible_text(value)
