from django.contrib.auth import get_user_model
from network.tests.factories import UserFactory

from .base import FunctionalTest

User = get_user_model()


class LoginTest(FunctionalTest):

    def wait_for_register_page_from_nav_bar(self):
        """
        Find Register button in nav bar, and wait for register page
        to load
        """
        register_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Register"]'
        )
        register_link.click()

        self.wait_for_url_to_load('/register/')

    def register_user_info_and_click_register(
            self, username, email, password, confirmation
    ):
        """
        On the Register page, enter the supplied username, email, password
        and password confirmation and click the register button
        """
        register_form_boxes = self.browser.find_elements_by_xpath(
            "//form[@action='/register/']/div//input"
        )
        username_box, email_box, password_box, confirmation_box, \
            = register_form_boxes

        username_box.send_keys(username)
        email_box.send_keys(email)
        password_box.send_keys(password)
        confirmation_box.send_keys(confirmation)

        register_button = self.browser.find_element_by_xpath(
            "//input[@value='Register']"
        )

        register_button.click()

    def test_user_can_create_new_account(self):
        """
        User goes to the homepage
        Isn't logged in (sees log in option)
        Clicks 'Register' button
        Is brought to the register page
        Enters valid information and clicks register
        Gets success notification and is redirected to homepage
        User is logged in (see log out option)
        """
        # User goes to the homepage
        self.browser.get(self.live_server_url)

        # Isn't logged in (sees log in option)
        self.check_user_logged_out()

        # Clicks 'Register' button in nav bar and is brought to register page
        self.wait_for_register_page_from_nav_bar()

        # Enters valid information and clicks register
        self.register_user_info_and_click_register(
            "harry", "hpotter@test.com", "P@ssword!", "P@ssword!"
        )

        # User gets success notification and is redirected to homepage
        self.wait_for_url_to_load('/')

        self.wait_for_alert_message("New Account Created")

        # User is logged in (see log out option)
        self.check_user_logged_in()

        # User logs out
        self.log_out_user()

        self.wait_for_alert_message("Logged out successfully")

    def test_user_with_account_can_login(self):
        """
        User has account (Pre-authenticated account created)
        Clicks log in nav bar
        brought to the login page
        Enters account email & password
        Clicks log in
        Gets success notification and is redirected to homepage
        User is logged in (see log out option)
        Logs in with account
        """
        # User has account (Pre-authenticated account created)
        user = UserFactory()

        self.browser.get(self.live_server_url)

        # user logs in
        self.log_in_user(user)

        # User gets success notification and is redirected to homepage
        self.wait_for_alert_message("Log In Complete")

        # User logs out
        self.log_out_user()

        self.wait_for_alert_message("Logged out successfully")

    def test_user_cannot_create_duplicate_account(self):
        """
        User has account (Pre-authenticated account created)
        User goes to the homepage
        Isn't logged in (sees log in option)
        Clicks 'Register' button
        Is brought to the register page
        Enters username for account already created and clicks register
        Gets error notification and is redirected to login page
        User is not logged in (see log in option)
        """
        # User has account (Pre-authenticated account created)
        UserFactory(username='harry')

        # User goes to the homepage
        self.browser.get(self.live_server_url)

        # User isn't logged in (sees log in option)
        self.check_user_logged_out()

        # Clicks 'Register' button in nav bar and is brought to register page
        self.wait_for_register_page_from_nav_bar()

        # Enters duplicate information and clicks register
        self.register_user_info_and_click_register(
            "harry", "hpotter@test.com", "P@ssword!", "P@ssword!"
        )

        # User gets error message and stays on register page
        self.assertRegex(self.browser.current_url, '/register')

        self.wait_for_alert_message("A user with that username already exists")

        # User isn't logged in (sees log in option)
        self.check_user_logged_out()
