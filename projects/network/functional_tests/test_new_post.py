from django.contrib.auth import get_user_model
from network.tests.factories import UserFactory

from .base import FunctionalTest

User = get_user_model()


class NewPostTest(FunctionalTest):

    def test_user_can_create_a_new_post(self):

        # User has an account
        user = UserFactory(username='harry')

        # User loads the home page
        self.browser.get(self.live_server_url)

        # User is not logged in
        self.check_user_logged_out()

        # Cannot see the New Post button in the navbar
        new_post_links = self.browser.find_elements_by_xpath(
            '//a[@class="nav-link"][text()="New Post"]'
        )
        self.wait_for(lambda: self.assertEqual(
            new_post_links, []
        ))

        # User logs in
        self.log_in_user(user)

        # Can see the New Post button in the navbar
        new_post_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="New Post"]'
        )
        new_post_link.click()

        self.wait_for_url_to_load('/new_post/')

        # Fills in text and clicks submit

        new_post_box = self.browser.find_element_by_xpath(
            "//form[@action='/new_post/']/div//textarea"
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
        self.wait_for(lambda: self.assertIn("Likes: 0", page_text))
