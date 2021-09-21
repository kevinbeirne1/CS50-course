# from django.contrib.auth import get_user_model
# from network.tests.factories import PostFactory, UserFactory

import datetime
import re

from .base import FunctionalTest, PreCreatedPostsFunctionalTest


class ProfileTest(PreCreatedPostsFunctionalTest):

    def test_profile_page_content(self):
        """
        Anonymous user loads harry's profile page and sees
        - only harry's posts
        - all harry's posts
        - in reverse chronological order
        - Number of harry's followers
        - Number of people harry follows
        """
        self.browser.get(self.live_server_url + '/harry/')
        self.wait_for_url_to_load("/harry/")


        # The page only displays posts by harry
        posts = self.browser.find_elements_by_xpath("//*[@id='post_media']")
        self.assertEqual(len(posts), 2)

        # the posts are in reverse chronological order
        pub_dates = self.browser.find_elements_by_xpath("//*[@id='pub_date']")

        pub_dates = [re.search(r'.+\:\s(.+)', date.text).group(1) for date in pub_dates]
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

        # The page doesn't display a follow/unfollow button




