import time
from datetime import datetime
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

User = get_user_model()

from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5
SCREEN_DUMP_LOCATION = Path(__file__).parent/'screendumps'


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self) -> None:
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir()
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshoting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        folder = SCREEN_DUMP_LOCATION
        classname = self.__class__.__name__
        method = self._testMethodName
        windowid = self._windowid
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return f'{folder}/{classname}.{method}-window{windowid}-{timestamp}'

    @wait
    def wait_for(self, fn):
        return fn()

    def check_user_logged_out(self):
        """
        Verify that the user ISNT logged in
        """
        login_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Log In"]'
        )
        self.assertIn('Log In', login_link.text)

    def check_user_logged_in(self):
        """Verify that the user IS logged in"""
        logout_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Log Out"]'
        )
        self.assertIn('Log Out', logout_link.text)

    def wait_for_url_to_load(self, url):
        self.wait_for(lambda: self.assertRegex(
            self.browser.current_url, f'{url}$'
        ))

    def wait_for_alert_message(self, expected_message):
        """
        Wait for alert to appear with the provided alert message.
        Click to dismiss the alert and verify that the alert disappears
        """
        status_message = self.browser.find_element_by_xpath(
            '//*[starts-with(@class, "alert")]'
        )
        self.wait_for(lambda: self.assertIn(
            expected_message,
            status_message.text
        ))

        dismiss_alert_button = self.browser.find_element_by_xpath(
            "//button[@data-dismiss='alert']"
        )
        dismiss_alert_button.click()

        status_messages = self.browser.find_elements_by_xpath(
            '//*[starts-with(@class, "alert")]'
        )

        self.wait_for(lambda: self.assertEqual(len(status_messages), 0))


class LoggedInFunctionalTest(FunctionalTest):

    def setUp(self) -> None:
        user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='P@ssword!',
        )
        super(LoggedInFunctionalTest, self).setUp()
        self.client.force_login(user)
