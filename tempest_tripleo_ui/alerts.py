from tempest_tripleo_ui.core import SeleniumElement
from tempest_tripleo_ui.timer import Timer
from time import sleep
import logging

logger = logging.getLogger(__name__)
alert_success_close_button = SeleniumElement.by_xpath(
    '//div[contains(@class, "alert-success")]/button[@class="close"]')
alert_success = SeleniumElement.by_xpath(
    '//div[contains(@class, "alert-success")]')
alert_danger_close_button = SeleniumElement.by_xpath(
    '//div[contains(@class, "alert-danger")]/button[@class="close"]')
alert_danger = SeleniumElement.by_xpath(
    '//div[contains(@class, "alert-danger")]')

# the spinner that we see while waiting for dialogs to open etc'
spinner = SeleniumElement.by_xpath(
    '//div[contains(@class, "spinner")]')


def clear_success_message(timeout=3):
    if alert_success_close_button.wait_for_element(timeout) and \
            not alert_success_close_button.is_stale():
        try:
            logger.info("Clearing message: {}".format(
                alert_success.get_all_text()))
            alert_success_close_button.click()
        except BaseException:
            pass    # sometimes the message disappears in this critical moment
        return True

    return False


def clear_danger_message(timeout=3):
    if alert_danger_close_button.wait_for_element(timeout) and \
            not alert_danger_close_button.is_stale():
        logger.error("Clearing alert: {}".format(
            alert_danger.get_all_text()))
        alert_danger_close_button.click()
        return True

    return False


def clear_all_success_messages():
    while clear_success_message():
        sleep(2)


def clear_all_danger_messages():
    while clear_danger_message():
        sleep(2)


def wait_for_spinner(timeout=60, spinner_element=None):
    if not spinner_element:
        spinner_element = spinner
    timer = Timer("spinner")
    while spinner_element.wait_for_element(3) and \
            timer.get_duration() < timeout:
        sleep(1)

    # not using timer.assert_timer() because we're not interested
    # in the error message it generates
    return timer.get_duration() < timeout
