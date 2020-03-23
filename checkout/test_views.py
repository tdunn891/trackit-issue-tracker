from django.test import TestCase
from accounts.models import User


class TestCheckoutViews(TestCase):
    def setUp(self):
        # Every test needs access to this logged in user
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_get_checkout_page(self):
        page = self.client.get("/checkout/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "checkout.html")
