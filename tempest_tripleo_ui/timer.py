from time import time
import logging

logger = logging.getLogger(__name__)


class Timer(object):

    def __init__(self, operation_name, timeout=10):
        self.timer = time()
        self.operationName = operation_name
        self.timeout = timeout
        self.duration = None

    def assert_timer(self, message=None, take_screenshot=True):
        if self.timer is None:
            logger.error("trying to use the same timer twice - please "
                            "create a new timer to start a new measurement")
            return

        self.duration = time() - self.timer
        self.timer = None

        if self.duration > self.timeout:
            errMsg = ("operation '{}' took {} seconds, allowed timeout "
                      "is {} seconds").format(self.operationName,
                                              self.duration,
                                              self.timeout)
            if message is not None:
                errMsg += ": {}".format(message)
            logger.error(errMsg, take_screenshot=take_screenshot)
            return False

        return True

    def getDuration(self):
        if self.duration is not None:
            return self.duration

        return time() - self.timer
