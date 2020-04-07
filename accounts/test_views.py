from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from accounts.models import User, Profile


class TestAccountsViewsLoggedIn(TestCase):
    def setUp(self):
        # Every test refers to this logged in user
        username = 'testuser'
        password = '12345'
        self.user = User.objects.create_user(
            username=username, password=password)
        login = self.client.login(username=username, password=password)

    def test_get_user_profile_page(self):
        page = self.client.get("/accounts/profile/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "profile.html")

    def test_redirect_to_home_page_after_logout(self):
        page = self.client.get("/accounts/logout/")
        self.assertRedirects(page, "/")

    def test_redirect_to_tickets_after_successful_login(self):
        page = self.client.get("/accounts/logout/")
        self.assertRedirects(page, "/")

    # POSTS
    def test_staff_access_is_granted(self):
        response = self.client.post(
            "/accounts/grant_staff_access/{}/".format(self.user.id))
        user = get_object_or_404(User, pk=self.user.id)
        self.assertEqual(user.is_staff, True)
        self.assertRedirects(response, "/accounts/profile/")


class TestAccountsViewsNotLoggedIn(TestCase):
    def test_get_registration_page(self):
        page = self.client.get("/accounts/register/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "registration.html")

    def test_get_login_page(self):
        page = self.client.get("/accounts/login/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "login.html")
