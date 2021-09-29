from network.tests.factories import PostFactory, UserFactory

from .base import FunctionalTest


class LikeTest(FunctionalTest):

    def test_logged_in_user_can_like_a_post(self):
        """
        Logged in user
        - opens the home page
        - sees a post
        - sees like button
        - doesn't see unlike button
        - clicks like
        - like value increments
        - sees unlike button
        - doesn't see unlike button
        - reloads the page
        - like value remains at 1
        """

        PostFactory()
        user = UserFactory()

        # User loads the homepage
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(user)

        # Sees a post
        post = self.browser.find_element_by_xpath(".//*[@class='post_media']")

        # Sees a like button
        like_button = post.find_element_by_xpath(".//*[@id='like']")
        self.assertTrue(like_button.is_displayed())

        likes_count = post.find_element_by_xpath(".//*[@id='likes_count']")
        self.assertEqual(likes_count.text, "0")

        # Doesn't see an unlike button
        unlike_button = post.find_element_by_xpath(".//*[@id='unlike']")
        self.assertFalse(unlike_button.is_displayed())

        # Clicks like
        like_button.click()

        # Likes value increments
        self.assertEqual(likes_count.text, "1")

        # Sees unlike button
        self.assertTrue(unlike_button.is_displayed())

        # Doesn't see like button
        self.assertFalse(like_button.is_displayed())

        # Reloads the page
        self.browser.refresh()

        # Likes_count remains at new value
        likes_count = self.browser.find_element_by_xpath("//*[@id='likes_count']")
        self.assertEqual(likes_count.text, "1", msg="likes_count reset after page reload")

    def test_logged_in_user_can_unlike_a_post(self):
        """
        Logged in user
        - opens the home page
        - sees a post they have liked
        - sees unlike button
        - doesn't see like button
        - clicks unlike
        - like value decrements
        - sees like button
        - doesn't see like button
        - reloads the page
        - like value remains at 0
        """

        post = PostFactory()
        user = UserFactory()
        post.likes.add(user)

        # User loads the homepage
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(user)

        # Sees a post
        post = self.browser.find_element_by_xpath(".//*[@class='post_media']")

        # Sees an unlike button
        unlike_button = post.find_element_by_xpath(".//*[@id='unlike']")
        self.assertTrue(unlike_button.is_displayed())

        likes_count = post.find_element_by_xpath(".//*[@id='likes_count']")
        self.assertEqual("1", likes_count.text)

        # Doesn't see a like button
        like_button = post.find_element_by_xpath(".//*[@id='like']")
        self.assertFalse(like_button.is_displayed())

        # Clicks unlike
        unlike_button.click()

        # Likes value decrements
        self.assertEqual(likes_count.text, "0")

        # Sees like button
        self.assertTrue(like_button.is_displayed())

        # Doesn't see unlike button
        self.assertFalse(unlike_button.is_displayed())

        # Reloads the page
        self.browser.refresh()

        # Likes_count remains at new value
        likes_count = self.browser.find_element_by_xpath("//*[@id='likes_count']")
        self.assertEqual(likes_count.text, "0", msg="likes count reset after reload")

    def test_logged_out_user_cannot_like_post(self):
        """
        Anonymous user
        - opens the home page
        - sees a post
        - doesn't see like button
        - doesn't see unlike button
        """
        PostFactory()

        # Anonymous User loads the homepage
        self.browser.get(self.live_server_url)

        # Sees a post
        post = self.browser.find_element_by_xpath("//*[@class='post_media']")

        # Doesn't see a like button
        like_buttons = post.find_elements_by_xpath(".//*[@id='like']")
        self.assertEqual(like_buttons, [])

        # Doesn't see an unlike button
        unlike_button = post.find_elements_by_xpath(".//*[@id='unlike']")
        self.assertEqual(unlike_button, [])
