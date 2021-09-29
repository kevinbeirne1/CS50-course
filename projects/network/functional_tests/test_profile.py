import re

from network.tests.factories import PostFactory, UserFactory

from .base import FunctionalTest


class ProfileTest(FunctionalTest):

    def setUp(self) -> None:
        super().setUp()
        PostFactory.create_batch(2, creator=UserFactory(username='harry'))
        PostFactory()

    def test_logged_out_profile_page_content(self):
        """
        Anonymous user loads harry's profile page and sees
        - only harry's posts
        - all harry's posts
        - in reverse chronological order
        - Number of harry's followers
        - Number of people harry follows
        - Doesn't see a follow/unfollow button
        """
        self.browser.get(self.live_server_url + '/harry/')
        self.wait_for_url_to_load("/harry/")

        # The page displays harry's profile name
        profile_name = self.browser.find_element_by_xpath("//*[@id='profile_name']")
        self.assertEqual(profile_name.text, 'harry')
        self.assertTrue(profile_name.is_displayed())

        # The page only displays posts by harry
        posts = self.browser.find_elements_by_xpath("//*[@class='post_media']")
        self.assertEqual(len(posts), 2)

        # the posts are in reverse chronological order
        pub_dates = self.browser.find_elements_by_xpath("//*[@id='pub_date']")

        pub_dates = [re.search(r'.+:\s(.+)', date.text).group(1) for date in pub_dates]
        second_post_date, first_post_date = pub_dates
        self.assertGreater(second_post_date, first_post_date)

        # The page displays the number of followers that harry has
        followers = self.browser.find_element_by_xpath(
            "//div[@id='profile_details']//*[@id='followers']"
        )
        self.assertEqual(followers.text, "Followers: 0")

        # The page displays the number of accounts harry follows
        followers = self.browser.find_element_by_xpath(
            "//div[@id='profile_details']//*[@id='following']"
        )
        self.assertEqual(followers.text, "Following: 0")

        # The page doesn't display a follow button
        follow_buttons = self.browser.find_elements_by_xpath("//*[id='follow']")
        self.assertEqual(follow_buttons, [])

        # The page doesn't display an unfollow button
        unfollow_buttons = self.browser.find_elements_by_xpath("//*[id='unfollow']")
        self.assertEqual(unfollow_buttons, [])

    def test_logged_in_profile_page_content(self):
        """
        logged in user loads harry's profile page and sees
        - only harry's posts
        - all harry's posts
        - in reverse chronological order
        - Number of harry's followers
        - Number of people harry follows
        - Doesn't see a follow/unfollow button
        """
        user = UserFactory()
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(user)

        # Opens harrys page
        self.browser.get(self.live_server_url + '/harry/')
        self.wait_for_url_to_load("/harry/")

        # The page displays harry's profile name
        profile_name = self.browser.find_element_by_xpath("//*[@id='profile_name']")
        self.assertEqual(profile_name.text, 'harry')
        self.assertTrue(profile_name.is_displayed())

        # The page only displays posts by harry
        posts = self.browser.find_elements_by_xpath("//*[@class='post_media']")
        self.assertEqual(len(posts), 2)

        # the posts are in reverse chronological order
        pub_dates = self.browser.find_elements_by_xpath("//*[@id='pub_date']")

        pub_dates = [re.search(r'.+:\s(.+)', date.text).group(1) for date in pub_dates]
        second_post_date, first_post_date = pub_dates
        self.assertGreater(second_post_date, first_post_date)

        # The page displays the number of followers that harry has
        followers = self.browser.find_element_by_xpath(
            "//div[@id='profile_details']//*[@id='followers']"
        )
        self.assertEqual(followers.text, "Followers: 0")

        # The page displays the number of accounts harry follows
        followers = self.browser.find_element_by_xpath(
            "//div[@id='profile_details']//*[@id='following']"
        )
        self.assertEqual(followers.text, "Following: 0")

        # The page displays a follow button
        follow_button = self.browser.find_element_by_xpath("//*[@id='follow']")
        self.assertTrue(follow_button.is_displayed())

        # The page doesn't display an unfollow button
        unfollow_button = self.browser.find_element_by_xpath("//*[@id='unfollow']")
        self.assertFalse(unfollow_button.is_displayed())

    def test_can_follow_account(self):
        """
        Logged in user
        - loads harry profile
        - harry doesn't have any followers
        - clicks follow button
        - harry's followers count increments
        - users following count increments on their profile
        - harry's posts are now shown in the following page
        """
        user = UserFactory(username='test_user')
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(user)

        # Opens harrys page
        self.browser.get(self.live_server_url + '/harry/')
        self.wait_for_url_to_load("/harry/")

        # Harry doens't have any followers
        followers_count = self.browser.find_element_by_xpath("//*[@id='followers_count']")
        self.assertEqual(followers_count.text, "0")

        # Clicks the follow button
        follow_button = self.browser.find_element_by_xpath("//*[@id='follow']")
        follow_button.click()

        # Harry's followers count increments
        self.assertEqual(followers_count.text, '1')

        # User opens their profile page
        profile_url = f"{self.live_server_url}/{user.username}/"
        self.browser.get(profile_url)
        self.wait_for_url_to_load(profile_url)

        # Users following count increments
        following_count = self.browser.find_element_by_xpath("//*[@id='following_count']")
        self.assertEqual(following_count.text, '1')

        # User opens the following page
        self.browser.get(self.live_server_url + "/following/")
        self.wait_for_url_to_load('/following/')

        # harry's posts are now shown
        creators = self.browser.find_elements_by_xpath("//*[@id='creator']")
        for creator in creators:
            with self.subTest():
                self.assertEqual(creator.text, 'harry')

    def test_can_unfollow_account(self):
        """
        Logged in user
        - follows harry
        - harry's posts are shown in the following page
        - loads harry profile
        - harry has 1 follower
        - clicks unfollow button
        - harry's followers count decrements
        - users following count decrements on their profile
        - harry's posts are not shown in the following page

        """
        # user follows harry
        user = UserFactory(username='test_user')
        harry = UserFactory(username='harry')
        user.following.add(harry)

        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(user)

        # User opens their profile page
        profile_url = f"{self.live_server_url}/{user.username}/"
        self.browser.get(profile_url)
        self.wait_for_url_to_load(profile_url)

        # User's following_count is 1
        following_count = self.browser.find_element_by_xpath("//*[@id='following_count']")
        self.assertEqual(following_count.text, '1')

        # User opens the following page
        self.browser.get(self.live_server_url + "/following/")
        self.wait_for_url_to_load('/following/')

        # harry's posts are shown
        creators = self.browser.find_elements_by_xpath("//*[@id='creator']")
        for creator in creators:
            with self.subTest():
                self.assertEqual(creator.text, 'harry')

        # Opens harrys page
        self.browser.get(self.live_server_url + '/harry/')
        self.wait_for_url_to_load("/harry/")

        # Harry has 1 followers
        followers_count = self.browser.find_element_by_xpath("//*[@id='followers_count']")
        self.assertEqual(followers_count.text, "1")

        # Clicks the follow button
        unfollow_button = self.browser.find_element_by_xpath("//*[@id='unfollow']")
        unfollow_button.click()

        # Harry's followers count decrements
        self.assertEqual(followers_count.text, '0')

        # User opens their profile page
        # profile_url = f"{self.live_server_url}/{user.username}/"
        self.browser.get(profile_url)
        self.wait_for_url_to_load(profile_url)

        # Users following count decrements
        following_count = self.browser.find_element_by_xpath("//*[@id='following_count']")
        self.assertEqual(following_count.text, '0')

        # User opens the following page
        self.browser.get(self.live_server_url + "/following/")
        self.wait_for_url_to_load('/following/')

        # harry's posts are now shown
        creators = self.browser.find_elements_by_xpath("//*[@id='creator']")
        self.assertEqual(creators, [])

    def test_user_cannot_follow_or_unfollow_themselves(self):
        """
        Logged in user
        - loads their profile
        - doesn't see a follow/unfollow button
        """
        user = UserFactory(username='test_user')
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(user)

        # Opens their profile page
        self.browser.get(f"{self.live_server_url}/{user.username}/")
        self.wait_for_url_to_load(f"/{user.username}/")

        # The page doesn't display a follow button
        follow_buttons = self.browser.find_elements_by_xpath("//*[@id='follow']")
        self.assertEqual(follow_buttons, [])

        # The page doesn't display an unfollow button
        unfollow_buttons = self.browser.find_elements_by_xpath("//*[@id='unfollow']")
        self.assertEqual(unfollow_buttons, [])
