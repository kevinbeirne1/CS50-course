import time
from datetime import datetime
from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from network.tests.factories import PostFactory, UserFactory
from selenium import webdriver
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
        options.add_argument('--headless')
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
        PostFactory.reset_sequence()

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

    def log_in_user(self, user):
        """Log provided user into selenium browser"""
        # Isn't logged in (sees log in option)
        login_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Log In"]'
        )
        self.assertIn('Log In', login_link.text)

        # Clicks log in nav bar
        login_link.click()

        # brought to the login page
        self.wait_for(lambda: self.assertRegex(
            self.browser.current_url, '/login/'
        ))

        # Enters account email & password
        login_form_boxes = self.browser.find_elements_by_xpath(
            "//form[@action='/login/']/div//input"
        )
        username_box, password_box = login_form_boxes

        username_box.send_keys(user.username)
        password_box.send_keys("P@ssword!")

        login_button = self.browser.find_element_by_xpath(
            "//input[@value='Log In']"
        )

        # Clicks log in
        login_button.click()

        # User is logged in (see log out option)
        self.check_user_logged_in()

    def log_out_user(self):
        """Log user out of selenium browser"""
        logout_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Log Out"]'
        )
        logout_link.click()

        # User is logged out (see log in option)
        self.check_user_logged_out()

    def wait_for_url_to_load(self, url):
        """
        Wait for provided url to load & verify that 404 error not raised
        """
        self.wait_for(lambda: self.assertRegex(
            self.browser.current_url, f'{url}$'
        ))
        body = self.browser.find_element_by_xpath("//body").text
        self.assertNotIn('not found', body.lower())

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

        # Wait for message to clear on chrome
        time.sleep(0.4)

        status_messages = self.browser.find_elements_by_xpath(
            '//*[starts-with(@class, "alert")]'
        )

        self.wait_for(lambda: self.assertEqual(len(status_messages), 0))


class PreCreatedPostsFunctionalTest(FunctionalTest):


    def setUp(self) -> None:
        """Pre create posts to display in index view"""
        super(PreCreatedPostsFunctionalTest, self).setUp()
        PostFactory.create_batch(6)
        PostFactory.create_batch(2, creator=UserFactory(username='harry'))
