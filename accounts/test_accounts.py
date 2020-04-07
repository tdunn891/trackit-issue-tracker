
from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from accounts.models import User, Profile


class TestAccountsModels(TestCase):
    def setUp(self):
        # Every test refers to this logged in user
        username = 'testuser'
        password = '12345'
        self.user = User.objects.create_user(
            username=username, password=password)
        login = self.client.login(username=username, password=password)

    def test_profile_class_returns_username(self):
        user = get_object_or_404(Profile, pk=self.user.id)
        self.assertEqual(str(user), user.user.username)
