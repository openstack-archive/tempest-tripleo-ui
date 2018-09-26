import logging
# from conf import Conf


logger = None


def getLogger():
    global logger
    if logger is not None:
        return logger

    logger = Log()
    return logger


def log(text):
    getLogger().log(text)


def logDebug(text):
    getLogger().logDebug(text)


def logWarning(text):
    getLogger().logWarning(text)


def logError(text, take_screenshot=True):
    getLogger().logError(text, take_screenshot)


def assertion(cond, text, take_screenshot=True):
    getLogger().assertion(cond, text, take_screenshot)


def setLoggingLevelInfo():
    getLogger().setLoggingLevelInfo()


def setLoggingLevelDebug():
    getLogger().setLoggingLevelDebug()


def setLoggingLevelWarning():
    getLogger().setLoggingLevelWarning()


def setLoggingLevelError():
    getLogger().setLoggingLevelError()


def reset_error_counter():
    getLogger().reset_error_counter()


def get_error_counter():
    return getLogger().get_error_counter()


class Log(object):
    def __init__(self):
        self.error_counter = 0
        self.log_debug = False

        logging_level = None #Conf().get_item("logger", "level")
        if logging_level is None:
            return
        elif logging_level == "info":
            self.setLoggingLevelInfo()
        elif logging_level == "warning":
            self.setLoggingLevelWarning()
        # NOTE: we're turning debug messages into info messages, so we'll
        # only see our debugging lines and not Sleniums's or Paramiko's...
        elif logging_level == "debug":
            self.setLoggingLevelInfo()
            self.log_debug = True
        elif logging_level == "error":
            self.setLoggingLevelError()
        else:
            self.logWarning("logging level {} unknown, check "
                            "your conf file".format(logging_level))

    def log(self, text):
        logging.info(text)

    def logDebug(self, text):
        # NOTE: we're turning debug messages into info messages, so we'll
        # only see our debugging lines and not Sleniums's or Paramiko's...
        if self.log_debug:
            self.log("DEBUG:" + text)

    def logWarning(self, text):
        logging.warning(text)

    def logError(self, text, take_screenshot=True):
        self.error_counter += 1
        logging.error(text)
        if take_screenshot:
            from tempest.gui.services import browser
            browser.save_screenshot()

    def assertion(self, cond, text, take_screenshot=True):
        if not cond:
            if take_screenshot:
                from tempest.gui.services import browser
                filename = browser.save_screenshot()
                text += "  [[screenshot: {}]]".format(filename)

#             from services.connector import close as close_connector
#             close_connector()
            assert False, text

    def setLoggingLevelInfo(self):
        logging.basicConfig(level=logging.INFO)

    def setLoggingLevelDebug(self):
        logging.basicConfig(level=logging.DEBUG)

    def setLoggingLevelWarning(self):
        logging.basicConfig(level=logging.WARNING)

    def setLoggingLevelError(self):
        logging.basicConfig(level=logging.ERROR)

    def get_error_counter(self):
        return self.error_counter

    def reset_error_counter(self):
        self.error_counter = 0

