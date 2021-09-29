from datetime import datetime

from django.contrib.auth import get_user_model
from network.tests.factories import PostFactory, UserFactory

from .base import FunctionalTest

User = get_user_model()


class AllPostsTest(FunctionalTest):

    def setUp(self) -> None:
        super().setUp()
        PostFactory.create_batch(2, creator=UserFactory(username='harry'))
        PostFactory()

    def test_logged_user_can_access_following_from_masthead(self):
        """
        anonymous user
        - clicks on all posts in masthead
        - assert index page loads successfully
        """
        # Load the homepage
        self.browser.get(self.live_server_url)

        # Anonymous user does not see "Following" in the masthead
        all_posts_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="All Posts"]'
        )

        # User clicks "All Posts" in the masthead
        all_posts_link.click()

        self.wait_for_url_to_load('/')

    def test_index_post_content(self):
        """
        Anonymous user
        - loads homepage
        - sees each post in separate container
        - Each post has:
          - Username of poster
          - Content of post
          - date & time of post
          - No likes for post
        """

        # User loads the homepage
        self.browser.get(self.live_server_url)

        # All posts are displayed on the homepage
        posts = self.browser.find_elements_by_xpath('//*[@class="post_media"]')
        self.assertEqual(len(posts), 3)

        for post in posts:
            with self.subTest():
                content = post.find_element_by_xpath(".//*[@id='content']").text
                creator = post.find_element_by_xpath(".//*[@id='creator']").text
                pub_date = post.find_element_by_xpath(".//*[@id='pub_date']").text
                likes = post.find_element_by_xpath(".//*[@id='likes']").text

                self.assertRegex(content, r"Post #\d")
                self.assertRegex(creator, ".+")
                self.assertRegex(pub_date, "Date Posted: .+")
                self.assertRegex(likes, "Likes: 0")

    def test_can_view_user_profile_from_index(self):
        """
        Anonymous user:
        - opens the homepage
        - sees post creators listed under their posts
        - clicks on the user 'harry's name
        - 'harry's profile loads
        """

        # User loads the home page
        self.browser.get(self.live_server_url)

        # User can see the profile name on a post
        profile_links = self.browser.find_elements_by_xpath(
            "//a[@id='creator']"
        )
        self.assertNotEqual(profile_links, [])

        # User clicks the first profile link
        harry_profile = self.browser.find_element_by_xpath("//*[text()='harry']")
        harry_profile.click()

        self.wait_for_url_to_load("/harry/")

    def test_posts_in_chronological_order(self):
        """
        Anonymous user:
        - opens homepage
        - sees posts in chronological order
        """
        # User loads the home page
        self.browser.get(self.live_server_url)

        pub_dates_elements = self.browser.find_elements_by_xpath(
            "//*[@id='pub_date']")
        pub_dates_strings = (pub_date.text.split(': ')[1] for
                             pub_date in pub_dates_elements)
        pub_dates = [datetime.strptime(pub_date, "%d, %b, %Y %H:%M") for
                     pub_date in pub_dates_strings]

        for i, pub_date in enumerate(pub_dates[:-1]):
            with self.subTest():
                self.assertGreater(pub_date, pub_dates[i + 1])


class FollowingTest(FunctionalTest):

    def setUp(self) -> None:
        """
        Create user account, and follow accounts belonging to 'harry'
        and 3 other users
        :return:
        """
        super().setUp()
        PostFactory.create_batch(3)
        PostFactory(creator=UserFactory(username='harry'))
        self.user = UserFactory()
        follows = list(User.objects.exclude(username=self.user.username))
        [self.user.following.add(follow) for follow in follows]

    def test_logged_user_can_access_following_from_masthead(self):
        """
        logged in user
        - clicks on following in masthead
        - assert page loads successfully
        """
        # Load the homepage
        self.browser.get(self.live_server_url)

        # Anonymous user does not see "Following" in the masthead
        following_links = self.browser.find_elements_by_xpath(
            '//a[@class="nav-link"][text()="Following"]'
        )
        self.assertEqual(following_links, [])

        # User is logged in
        self.log_in_user(UserFactory())

        # User clicks "Following" in the masthead
        following_link = self.browser.find_element_by_xpath(
            '//a[@class="nav-link"][text()="Following"]'
        )
        following_link.click()

        self.wait_for_url_to_load('/following/')

    def test_anonymous_user_cant_access_following(self):
        """
        Anonymous user:
        - attempts to load '/following/'
        - redirected to index '/'
        - Error message appears
        """
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        self.wait_for_url_to_load('/login/')

        self.wait_for_alert_message("Login Required")

    def test_logged_in_user_can_access_following(self):
        """
        logged in user
        - attempts to load '/following/'
        - webpage loads
        """

        # Load the homepage
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(self.user)

        # User loads 'following'
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        self.wait_for_url_to_load('/following/')

    def test_following_lists_all_posts_accounts_user_follows(self):
        """
        logged in user
        - loads following
        - All posts by following accounts are lists
        """
        # Load the homepage
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(self.user)

        # User loads 'following'
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        self.wait_for_url_to_load('/following/')

        # All posts are displayed on the homepage
        posts = self.browser.find_elements_by_xpath('//*[@class="post_media"]')
        self.assertEqual(len(posts), 4)

    def test_following_post_content(self):
        """
        logged in user
        - loads following
        - sees each post in separate container
        - Each post has:
          - Username of poster
          - Content of post
          - date & time of post
          - No likes for post
        """
        # User loads the homepage
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(self.user)

        # User loads 'following'
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        self.wait_for_url_to_load('/following/')

        # All posts display the correct information
        posts = self.browser.find_elements_by_xpath('//*[@class="post_media"]')

        for post in posts:
            with self.subTest():
                content = post.find_element_by_xpath(".//*[@id='content']").text
                creator = post.find_element_by_xpath(".//*[@id='creator']").text
                pub_date = post.find_element_by_xpath(".//*[@id='pub_date']").text
                likes = post.find_element_by_xpath(".//*[@id='likes']").text

                self.assertRegex(content, r"Post #\d")
                self.assertRegex(creator, ".+")
                self.assertRegex(pub_date, "Date Posted: .+")
                self.assertRegex(likes, "Likes: 0")

    def test_can_view_user_profile_from_following(self):
        """
        Logged in user:
        - opens the following page
        - sees post creators listed under their posts
        - clicks on the user 'harry's name
        - 'harry's profile loads
        """

        # User loads the home page
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(self.user)

        # User loads 'following'
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        self.wait_for_url_to_load('/following/')

        # User can see the profile name on a post
        profile_links = self.browser.find_elements_by_xpath(
            "//a[@id='creator']"
        )
        self.assertNotEqual(profile_links, [])

        # User clicks the first profile link
        profile_links[0].click()

        self.wait_for_url_to_load("/harry/")

    def test_posts_in_chronological_order(self):
        """
        Logged in user:
        - opens the following page
        - sees posts in chronological order
        """
        # User loads the home page
        self.browser.get(self.live_server_url)

        # User is logged in
        self.log_in_user(self.user)

        # User loads 'following'
        following_url = self.live_server_url + '/following/'
        self.browser.get(following_url)

        self.wait_for_url_to_load('/following/')

        pub_dates_elements = self.browser.find_elements_by_xpath(
            "//*[@id='pub_date']")
        pub_dates_strings = (pub_date.text.split(': ')[1] for
                             pub_date in pub_dates_elements)
        pub_dates = [datetime.strptime(pub_date, "%d, %b, %Y %H:%M") for
                     pub_date in pub_dates_strings]

        for i, pub_date in enumerate(pub_dates[:-1]):
            with self.subTest():
                self.assertGreater(pub_date, pub_dates[i + 1])
