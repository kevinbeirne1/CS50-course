from network.tests.factories import PostFactory, UserFactory

from .base import FunctionalTest


class PaginationTest(FunctionalTest):

    def tearDown(self) -> None:
        super().tearDown()
        PostFactory.reset_sequence()

    def pagination_test(self):
        """
        Helper function for testing pagination
        - Test that each page has up to 10 posts
        - First page has Next button
        - Middle pages have Next & Previous buttons
        - Last page has only Previous button
        - Cycle through all the pages with buttons
          - Making sure each page loads
        """

        # Sees 10 posts in the page
        page1_posts = self.browser.find_elements_by_xpath('//*[@class="post_media"]')

        self.assertEqual(len(page1_posts), 10)

        # Doesn't see Previous button
        previous_buttons = self.browser.find_elements_by_link_text('Previous')
        self.assertEqual(previous_buttons, [])

        # Sees Next button & clicks
        next_button = self.browser.find_element_by_link_text('Next')
        next_button.click()

        # Page 2 loads
        self.wait_for_url_to_load('/?page=2')

        # Sees 10 posts in the second page
        page2_posts = self.browser.find_elements_by_xpath('//*[@class="post_media"]')
        self.assertEqual(len(page2_posts), 10)

        self.assertNotEqual(page2_posts, page1_posts)

        # Sees Previous button
        self.browser.find_element_by_link_text('Previous')

        # Sees Next button and clicks
        next_button = self.browser.find_element_by_link_text('Next')
        next_button.click()

        # Page 3 loads
        self.wait_for_url_to_load('/?page=3')

        # Sees 2 posts in the second page
        page3_posts = self.browser.find_elements_by_xpath('//*[@class="post_media"]')
        self.assertEqual(len(page3_posts), 2)

        # Doesn't see Next button
        next_buttons = self.browser.find_elements_by_link_text('Next')
        self.assertEqual(next_buttons, [])

        # Sees Previous button and clicks
        previous_button = self.browser.find_element_by_link_text('Previous')
        previous_button.click()

        # Page 2 loads
        self.wait_for_url_to_load('/?page=2')

        # Sees Previous button and clicks
        previous_button = self.browser.find_element_by_link_text('Previous')
        previous_button.click()

        # Page 1 loads
        self.wait_for_url_to_load('/?page=1')

    def test_all_posts_pagination(self):
        """
        Anonymous user:
        - opens the home page
        - see only 10 posts in page
        - clicks next
        - sees next 10 posts
        - sees next & back buttons
        - clicks next
        - sees last 2 posts
        - only sees back button
        """
        PostFactory.create_batch(22)

        # User loads the homepage
        self.browser.get(self.live_server_url)

        # Test pagination on homepage
        self.pagination_test()

    def test_profile_pagination(self):
        """
        Anonymous user:
        - opens the 'test_user's profile page
        - see only 10 posts in page
        - clicks next
        - sees next 10 posts
        - sees next & back buttons
        - clicks next
        - sees last 2 posts
        - only sees back button
        """
        PostFactory.create_batch(22, creator=UserFactory(username='test_user'))

        # User loads 'test_user's profile page
        profile_url = self.live_server_url + '/test_user/'
        self.browser.get(profile_url)

        # Test pagination of /profile/<profile_name>
        self.pagination_test()

    def test_following_pagination(self):
        """
        Logged in user:
        - opens the following page
        - see only 10 posts in page
        - clicks next
        - sees next 10 posts
        - sees next & back buttons
        - clicks next
        - sees last 2 posts
        - only sees back button
        """

        test_user = UserFactory()
        followed_user = UserFactory(username='followed_user')
        PostFactory.create_batch(22, creator=followed_user)

        test_user.following.add(followed_user)

        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(test_user)

        # User loads 'test_user's profile page
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        # Test pagination of "/following/
        self.pagination_test()
