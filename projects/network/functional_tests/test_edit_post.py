from time import sleep
from unittest import skip

from network.tests.factories import PostFactory, UserFactory
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class EditPostTest(FunctionalTest):

    def test_edit_own_post(self):
        """
        Logged in user
        - loads homepage
        - sees their post
        - clicks edit button
        - text is replaced by a text area
        - user changes the content
        - clicks save
        - post changes back to text
        - post is updated
        - reloads the page
        - post is has not reverted to old version
        """
        # user has account and posts
        user = UserFactory(username='test_user')

        PostFactory.create_batch(3)
        PostFactory(creator=user, content="A new post")

        # User loads the home page
        self.browser.get(self.live_server_url)

        # user is logged in
        self.log_in_user(user)

        # sees their post
        post = self.browser.find_element_by_xpath(
                "//*[text()='test_user']/ancestor::*[@id='post_media']"
        )

        content = post.find_element_by_xpath("//*[@id='content']")
        textarea = post.find_element_by_xpath("//textarea")
        save_button = post.find_element_by_xpath("//*[@id='save']")
        edit_button = post.find_element_by_xpath("//*[@id='edit']")

        # Content is visible
        content_text = content.text
        self.assertEqual(content.is_displayed(), True)

        # Edit button is visible
        self.assertEqual(edit_button.is_displayed(), True)

        # Save button and textarea are not visible
        self.assertEqual(save_button.is_displayed(), False)
        self.assertEqual(textarea.is_displayed(), False)

        # User clicks the edit button
        edit_button.click()
        textarea = post.find_element_by_xpath("//textarea")

        # content value is displayed in text area
        textarea.is_displayed()
        self.assertEqual(content_text, textarea.text)

        # Save button is visible
        save_button.is_displayed()

        # content and edit_button are not visible
        self.assertEqual(content.is_displayed(), False)
        self.assertEqual(edit_button.is_displayed(), False)

        # user edits the post
        textarea.clear()
        textarea.send_keys("a post about something else")

        # Sanity Check that textarea has updated
        textarea_content = textarea.get_attribute('value')
        self.assertEqual(textarea_content, "a post about something else")

        # User clicks save
        save_button.click()

        # Content is visible
        self.assertEqual(content.is_displayed(), True)

        # Edit button is visible
        self.assertEqual(edit_button.is_displayed(), True)

        # Save button and textarea are not visible
        self.assertEqual(save_button.is_displayed(), False)
        self.assertEqual(textarea.is_displayed(), False)

        # content has updated to match the input textarea
        self.assertEqual(content.text, textarea_content)

        # The user reloads the page
        self.browser.refresh()

        # The post still displays the new content
        post = self.browser.find_element_by_xpath(
                "//*[text()='test_user']/ancestor::*[@id='post_media']"
        )

        content = post.find_element_by_xpath("//*[@id='content']")
        self.assertEqual(content.text, textarea_content)

    def test_edit_post_changes_only_one_post(self):
        """
        Logged in user
        - loads homepage
        - sees their 3 posts
        - only wants to change the second post
        - edits the 2nd post & clicks save
        - only the 2nd post is changed
        """
        # user has account and posts
        user = UserFactory(username='test_user')

        PostFactory.create_batch(3)
        PostFactory.create_batch(3, creator=user, content="A new post")

        # User loads the home page
        self.browser.get(self.live_server_url)

        # user is logged in
        self.log_in_user(user)

        # sees their 3 posts
        original_posts = self.browser.find_elements_by_xpath(
            "//*[text()='test_user']/ancestor::*[@id='post_media']"
        )
        self.assertEqual(len(original_posts), 3)

        # Only wants to change the second post
        post = original_posts[1]

        content = post.find_element_by_xpath("//*[@id='content']")
        textarea = post.find_element_by_xpath("//textarea")
        save_button = post.find_element_by_xpath("//*[@id='save']")
        edit_button = post.find_element_by_xpath("//*[@id='edit']")

        # Content is visible
        content_text = content.text
        self.assertEqual(content.is_displayed(), True)

        # Edit button is visible
        self.assertEqual(edit_button.is_displayed(), True)

        # Save button and textarea are not visible
        self.assertEqual(save_button.is_displayed(), False)
        self.assertEqual(textarea.is_displayed(), False)

        # User clicks the edit button
        edit_button.click()
        textarea = post.find_element_by_xpath("//textarea")

        # content value is displayed in text area
        textarea.is_displayed()
        self.assertEqual(content_text, textarea.text)

        # Save button is visible
        save_button.is_displayed()

        # content and edit_button are not visible
        self.assertEqual(content.is_displayed(), False)
        self.assertEqual(edit_button.is_displayed(), False)

        # user edits the post
        textarea.clear()
        textarea.send_keys("a post about something else")

        # Sanity Check that textarea has updated
        textarea_content = textarea.get_attribute('value')
        self.assertEqual(textarea_content, "a post about something else")

        # User clicks save
        save_button.click()

        # Content is visible
        self.assertEqual(content.is_displayed(), True)

        # Edit button is visible
        self.assertEqual(edit_button.is_displayed(), True)

        # Save button and textarea are not visible
        self.assertEqual(save_button.is_displayed(), False)
        self.assertEqual(textarea.is_displayed(), False)

        # content has updated to match the input textarea
        self.assertEqual(content.text, textarea_content)

        # only the second post is changed
        new_posts = self.browser.find_elements_by_xpath(
            "//*[text()='test_user']/ancestor::*[@id='post_media']"
        )
        new_posts = [post.text for post in new_posts]

        self.assertEqual(new_posts[0], original_posts[0].text)
        self.assertEqual(new_posts[2], original_posts[2].text)

        # The user reloads the page
        self.browser.refresh()

        # only the second post is changed
        posts = self.browser.find_elements_by_xpath(
            "//*[text()='test_user']/ancestor::*[@id='post_media']"
        )

        self.assertEqual(posts[0].text, new_posts[0])
        self.assertEqual(posts[1].text, new_posts[1])
        self.assertEqual(posts[2].text, new_posts[2])

    def test_anonymous_user_cannot_edit_posts(self):
        """
        Anonymous User:
        - loads homepage
        - sees a number of posts
        - cannot see/click the edit button
        """

        PostFactory.create_batch(3)

        # User loads the home page
        self.browser.get(self.live_server_url)

        # sees a number of posts
        posts = self.browser.find_elements_by_xpath(
            "//*[@id='post_media']"
        )
        self.assertNotEqual(posts, [])

        # Cannot see the edit button
        edit_buttons = self.browser.find_elements_by_xpath("//*[@id='edit']")
        self.assertEqual(edit_buttons, [])

    def test_logged_in_user_cannot_edit_other_users_posts(self):
        """
        Logged in User:
        - loads homepage
        - sees a number of posts
        - cannot see/click the edit button
        """
        # user has account
        user = UserFactory(username='test_user')

        PostFactory.create_batch(3)

        # User loads the home page
        self.browser.get(self.live_server_url)

        # user is logged in
        self.log_in_user(user)

        # sees a number of posts
        posts = self.browser.find_elements_by_xpath(
            "//*[@id='post_media']"
        )
        self.assertNotEqual(posts, [])

        # Cannot see the edit button
        edit_buttons = self.browser.find_elements_by_xpath("//*[@id='edit']")
        self.assertEqual(edit_buttons, [])

