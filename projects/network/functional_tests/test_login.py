from time import sleep
from unittest import skip

from django.contrib.auth import get_user_model
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest, wait

User = get_user_model()


class LoginTest(FunctionalTest):

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
            self.browser.current_url, url
        ))

    def wait_for_register_page_from_nav_bar(self):
        """
        Find Register button in nav bar, and wait for register page
        to load
        """
        register_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Register"]'
        )
        register_link.click()

        self.wait_for_url_to_load('/register')

    def register_user_info_and_click_register(
            self, username, email, password, confirmation
    ):
        """
        On the Register page, enter the supplied username, email, password
        and password confirmation and click the register button
        """
        register_form_boxes = self.browser.find_elements_by_xpath(
            "//form[@action='/register']/div//input"
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

    def wait_for_status_message(self, expected_message):
        status_message = self.browser.find_element_by_xpath(
            '//*[starts-with(@class, "alert")]'
        )
        self.wait_for(lambda: self.assertIn(
            expected_message,
            status_message.text
        ))

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
            "harry", "hpotter@test.com", "password", "password"
        )

        # User gets success notification and is redirected to homepage
        self.wait_for_url_to_load('/')

        self.wait_for_status_message("Success: New Account Created")

        # User is logged in (see log out option)
        self.check_user_logged_in()

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
        user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='password',
            )

        self.browser.get(self.live_server_url)

        # Isn't logged in (sees log in option)
        login_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Log In"]'
        )
        self.assertIn('Log In', login_link.text)

        # Clicks log in nav bar
        login_link.click()

        # brought to the login page
        self.wait_for(lambda: self.assertRegex(
            self.browser.current_url, '/login'
        ))

        # Enters account email & password
        login_form_boxes = self.browser.find_elements_by_xpath(
            "//form[@action='/login']/div//input"
        )
        username_box, password_box = login_form_boxes

        username_box.send_keys("harry")
        password_box.send_keys('password')

        login_button = self.browser.find_element_by_xpath(
            "//input[@value='Log In']"
        )

        # Clicks log in
        login_button.click()

        # User gets success notification and is redirected to homepage
        self.wait_for_url_to_load('/')

        self.wait_for_status_message("Success: Log In Complete")

        # User is logged in (see log out option)
        self.check_user_logged_in()

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

        user = User.objects.create_user(
            username='harry',
            email='hpotter@test.com',
            password='password',
        )

        # User goes to the homepage
        self.browser.get(self.live_server_url)

        # User isn't logged in (sees log in option)
        self.check_user_logged_out()

        # Clicks 'Register' button in nav bar and is brought to register page
        self.wait_for_register_page_from_nav_bar()

        # Enters duplicate information and clicks register
        self.register_user_info_and_click_register(
            "harry", "hpotter@test.com", "password", "password"
        )

        # User gets error message and stays on register page
        self.wait_for_url_to_load('/register')
        self.wait_for_status_message("Error: Username Already Taken")

        # User isn't logged in (sees log in option)
        self.check_user_logged_out()



