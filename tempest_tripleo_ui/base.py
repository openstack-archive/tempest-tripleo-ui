from tempest import test
from tempest_tripleo_ui.models import login
from tempest_tripleo_ui.services import browser
import logging

logger = logging.getLogger(__name__)


class GUITestCase(test.BaseTestCase):

    @classmethod
    def resource_setup(cls):
        """Login to the GUI. This will also open up the browser and get the
           home page - according to the parameters configured in the [UI]
           section in the conf file.
        """
        super(GUITestCase, cls).resource_setup()
        if not login.login():
            logger.error(
                "Unable to login to TripleO UI (check "
                "credentials in the tempest conf file)")
            # FIXME: throw an assertion here !!!

        cls.addClassResourceCleanup(cls.logout_and_close_browser)

    @classmethod
    def logout_and_close_browser(cls):
        if login.is_logged_in():
            login.logout()
        browser.quit_browser()
