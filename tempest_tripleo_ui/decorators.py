from functools import wraps
from selenium.common.exceptions import (
    StaleElementReferenceException, InvalidElementStateException
)
import logging

logger = logging.getLogger(__name__)


def selenium_action(f):
    """The selenium_action decorator

    This decorator can be used to wrap methods of ``SeleniumElement`` to
    provide exception handling, and automatic retries.

    It expects that the method being decorated accepts a ``webelement``
    as its first positional argument after ``self``.

    E.g.

        @selenium_action
        def click_button(self, webelement):
            ...
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        webelement = self.get_element()

        if not webelement:
            return

        try:
            try:
                return f(self, webelement, *args, **kwargs)
            except (StaleElementReferenceException,
                    InvalidElementStateException):
                logger.debug("stale element: {}".format(self.get_identifier_string()))
                self.wait_for_element(3)
                webelement = self.get_element()
                if webelement is None:
                    return None
                return f(self, webelement, *args, **kwargs)
        except Exception as e:
            logger.warning("selenium exception on '{}': {}"
                           .format(self.get_identifier_string(), e))
            raise
        return None

    return wrapper
