from time import sleep

from .base import FunctionalTest, LoggedInFunctionalTest


class NewPostTest(LoggedInFunctionalTest):

    def test_user_can_create_a_new_post(self):

        # User is not logged in
        self.client.logout()

        self.browser.get(self.live_server_url)

        self.check_user_logged_out()

        # Cannot see the New Post button in the navbar
        new_post_links = self.browser.find_elements_by_xpath(
            '//a[@class="nav-link"][text()="New Post"]'
        )
        self.wait_for(lambda: self.assertEqual(
            new_post_links, []
        ))

        # User logs in

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
        password_box.send_keys('P@ssword!')

        login_button = self.browser.find_element_by_xpath(
            "//input[@value='Log In']"
        )

        # Clicks log in
        login_button.click()

        # Can see the New Post button in the navbar
        new_post_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="New Post"]'
        )
        new_post_link.click()

        self.wait_for_url_to_load('/new_post')

        # Fills in text and clicks submit

        new_post_box = self.browser.find_element_by_xpath(
            "//form[@action='/new_post']/div//textarea"
        )
        new_post_box.send_keys("A new post")

        new_post_submit_button = self.browser.find_element_by_xpath(
            "//input[@value='Submit']"
        )

        new_post_submit_button.click()

        # User redirects to all posts

        self.wait_for_url_to_load('/')

        # Post is displayed on the all posts page

        page_text = self.browser.find_element_by_xpath('//*[body]').text
        self.wait_for(lambda: self.assertIn("A new post", page_text))
        self.wait_for(lambda: self.assertIn("Post Creator: harry", page_text))
        self.wait_for(lambda: self.assertIn("Date Posted: ", page_text))




