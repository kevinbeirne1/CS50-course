from django.test import Client, RequestFactory,TestCase
from django.urls import resolve, reverse
from django.urls.exceptions import NoReverseMatch

from . import views
from . import urls


class UrlsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url_paths = (
            "/",
            "/login",
            "/logout",
            "/register",
            "/following",
            "/edit",
            "/profile"
        )
        cls.no_of_urls = len(cls.url_paths)

    def test_number_urls(self):
        """
        Verify the number of urls to ensure full testing coverage
        """
        actual = len(urls.urlpatterns)
        expected = self.no_of_urls
        message = \
            "The no. of urlpatterns doesn't match the no. of test url_paths"
        self.assertEqual(actual, expected, message)

    def test_url_view_functions(self):
        """
        Test the various url names to verify their view functions
        """
        expected_functions = (
            views.IndexView,
            views.LoginView,
            views.LogoutView,
            views.RegisterView,
            views.FollowingView,
            views.EditView,
            views.ProfileView,
        )

        for url_path, expected in zip(self.url_paths, expected_functions):
            with self.subTest(i=url_path):
                resolver = resolve(url_path)
                view_function = resolver.func.view_class
                self.assertEqual(view_function, expected)

    def test_url_view_names(self):
        """
        Test the various url names to verify their view names
        """
        expected_names = (
            "index",
            "login",
            "logout",
            "register",
            "following",
            "edit",
            "profile",
        )

        for url_path, expected in zip(self.url_paths, expected_names):
            with self.subTest(i=url_path):
                resolver = resolve(url_path)
                view_name = resolver.url_name
                self.assertEqual(view_name, expected)

    def test_url_reverse(self):
        """
        Test the various names to verify their url value
        """

        url_names = (
            ('index', {}, '/'),
            ('login', {}, '/login'),
            ('logout', {}, '/logout'),
            ('register', {}, '/register'),
            ('following', {}, '/following'),
            ('edit', {}, '/edit'),
            ('profile', {'profile_name': 'test'}, '/test'),
        )

        for url_name, kwargs, expected in url_names:
            with self.subTest(i=url_name):
                url = reverse(url_name, kwargs=kwargs)
                self.assertEqual(url, expected)

    def test_profile_no_kwarg(self):
        """
        Verify that profile raises NoReverseMatch exception if profile not provided
        """
        with self.assertRaises(NoReverseMatch):
            reverse("profile")
