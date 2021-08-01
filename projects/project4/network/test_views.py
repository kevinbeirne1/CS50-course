from django.test import Client, RequestFactory,TestCase
from django.urls import reverse
from unittest import mock

from .models import Follow, Like, Post, User
from . import views
# from .views import index, login_view, logout_view, register, profile, edit, following


class ViewsTestCase(TestCase):

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

        pass

    def setUp(self):
        self.factory = RequestFactory()

    def test_view__get_templates(self):
        root_folder = "network/"
        expected_templates = (
            "index.html",
            "login.html",
            "index.html",
            "register.html",
            "following.html",
            "edit.html",
            "profile.html"
        )
        for url, expected in zip(self.url_paths, expected_templates):
            with self.subTest(i=url):
                response = self.client.get(url)
                if url == "/logout":
                    self.assertEqual(response.status_code, 302)
                    self.assertRedirects(response, "/")
                    continue
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, root_folder + expected)

    # def test_logout_redirect(self):
    #     response = self.client.get("/logout")
    #     self.assertEqual(response.status_code, )

    # def test_index_url_exists_at_desired_location(self):
    #     request = self.factory.get("/tst")
    #     print(request.path)
    #     response = views.ProfileView(request)
    #     print(request)
    #     print(response)
    #     self.assertEqual(response.status_code, 200)


    # def test_urls_exists_at_desired_locations(self):
    #     locations = (
    #         ("", index, "index.html"),
    #         ("login", login_view, "login.html"),
    #         ("logout", logout_view, ""),
    #         ("register", register), ("following", following),
    #         ("edit", edit))
    #
    #     root_path = "/network/"
    #     for location, view in locations:
    #         with self.subTest(i=location):
    #             request = self.factory.get(root_path + location)
    #             response = view(request)
    #             self.assertEqual(response.status_code, 200)
    #
    # def test_index_url_exists_at_desired_location(self):
    #
    #     request = self.factory.get("/network/")
    #     response = index(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_index_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('index'))
    #     response = index(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_login_url_exists_at_desired_location(self):
    #     request = self.factory.get("/network/login")
    #     response = login_view(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_login_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('login'))
    #     response = login_view(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_logout_url_exists_at_desired_location(self):
    #     request = self.factory.get("/network/logout")
    #     response = logout_view(request)
    #     # self.assertEqual(response.status_code, 200)
    #
    # def test_logout_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('logout'))
    #     response = logout_view(request)
    #     # self.assertEqual(response.status_code, 200)
    #
    # def test_register_url_exists_at_desired_location(self):
    #     request = self.factory.get("/network/register")
    #     response = register(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_register_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('register'))
    #     response = register(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "network/register.html")
    #
    # def test_profile_url_exists_at_desired_location(self):
    #     response = self.client.get("/test")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "network/profile.html")
    #
    # def test_profile_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('profile', kwargs={"profile_name": "test"}))
    #     response = profile(request, request.path)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_profile_url_exists_at_desired_location(self):
    #     request = self.factory.get("/network/test")
    #     response = profile(request, request.path)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_profile_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('profile', kwargs={"profile_name": "test"}))
    #     response = profile(request, request.path)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_various_potential_profile_names_and_errors(self):
    #     pass
    #
    # def test_following_url_exists_at_desired_location(self):
    #     request = self.factory.get("/network/following")
    #     response = following(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_following_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('following'))
    #     response = following(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_edit_url_exists_at_desired_location(self):
    #     request = self.factory.get("/network/following")
    #     response = following(request)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_edit_url_accessible_by_name(self):
    #     request = self.factory.get(reverse('following'))
    #     response = following(request)
    #     self.assertEqual(response.status_code, 200)
