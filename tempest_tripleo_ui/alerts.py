from tempest.gui.core import SeleniumElement
from services import logger
from tempest.gui.timer import Timer
from time import sleep


alertSuccessCloseButton = SeleniumElement.byXpath(
    '//div[contains(@class, "alert-success")]/button[@class="close"]')
alertSuccess = SeleniumElement.byXpath(
    '//div[contains(@class, "alert-success")]')
alertDangerCloseButton = SeleniumElement.byXpath(
    '//div[contains(@class, "alert-danger")]/button[@class="close"]')
alertDanger = SeleniumElement.byXpath(
    '//div[contains(@class, "alert-danger")]')

# the spinner that we see while waiting for dialogs to open etc'
spinner = SeleniumElement.byXpath(
    '//div[contains(@class, "spinner")]')


def clearSuccessMessage(timeout=3):
    if alertSuccessCloseButton.waitForElement(timeout) and \
            not alertSuccessCloseButton.isStale():
        try:
            logger.log("Clearing message: {}".format(
                alertSuccess.getAllText()))
            alertSuccessCloseButton.click()
        except BaseException:
            pass    # sometimes the message disappears in this critical moment
        return True

    return False


def clearDangerMessage(timeout=3):
    if alertDangerCloseButton.waitForElement(timeout) and \
            not alertDangerCloseButton.isStale():
        logger.logError("Clearing alert: {}".format(
            alertDanger.getAllText()))
        alertDangerCloseButton.click()
        return True

    return False


def clearAllSuccessMessages():
    while clearSuccessMessage():
        sleep(2)


def clearAllDangerMessages():
    while clearDangerMessage():
        sleep(2)


def waitForSpinner(timeout=60, spinner_element=None):
    logger.logDebug("waiting for spinners...")
    if not spinner_element:
        spinner_element = spinner
    timer = Timer("spinner")
    while spinner_element.waitForElement(3) and \
            timer.getDuration() < timeout:
        sleep(1)

    # not using timer.assert_timer() because we're not interested
    # in the error message it generates
    return timer.getDuration() < timeout
