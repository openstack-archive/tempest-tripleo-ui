from functools import wraps
from selenium.common.exceptions import (
    StaleElementReferenceException, InvalidElementStateException
)

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
        webelement = self.getElement()

        if not webelement:
            return

        try:
            try:
                return f(self, webelement, *args, **kwargs)
            except (StaleElementReferenceException,
                    InvalidElementStateException):
                self.waitForElement(3)
                webelement = self.getElement()
                if webelement is None:
                    return None
                return f(self, webelement, *args, **kwargs)
        except Exception as e:
            logger.warning("selenium exception on '{}': {}"
                              .format(self.get_name(), e))
            raise
        return None

    return wrapper
