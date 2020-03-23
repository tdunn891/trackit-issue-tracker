from django.test import TestCase
from .forms import MakePaymentForm, OrderForm


# class TestMakePaymentForm(TestCase):
#     def test_correct_message_for_missing_credit_card_number(self):
#         form = MakePaymentForm({'credit_card_number': ''})
#         self.assertFalse(form.is_valid)


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

    # def test_no_field_error_message_if_missing_street_address2(self):
    #     form = OrderForm({'street_address2': ''})
    #     self.assertFalse(form.errors['street_address2'])
        # self.assertFalse(form.is_valid())
