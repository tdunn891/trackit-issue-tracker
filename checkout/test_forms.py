from django.test import TestCase
from .forms import MakePaymentForm, OrderForm


class TestOrderForm(TestCase):
    def test_correct_message_for_missing_full_name(self):
        form = OrderForm({'full_name': ''})
        self.assertEqual(form.errors['full_name'], [
                         u'This field is required.'])
        self.assertFalse(form.is_valid())

    def test_correct_message_for_missing_street_address1(self):
        form = OrderForm({'street_address1': ''})
        self.assertEqual(form.errors['street_address1'], [
                         u'This field is required.'])
        self.assertFalse(form.is_valid())
