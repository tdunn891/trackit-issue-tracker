from django.test import TestCase
from .forms import AddTicketForm, EditTicketForm, AddCommentForm


class TestAddTicketForm(TestCase):
    def test_cannot_create_a_ticket_with_just_ticket_type_equals_bug(self):
        form = AddTicketForm({'ticket_type': 'Bug'})
        self.assertFalse(form.is_valid())

    def test_cannot_create_a_ticket_with_other_ticket_type(self):
        form = AddTicketForm({'ticket_type': 'Other'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ticket_type'],
                         [u'Select a valid choice. Other is not one of the available choices.'])

    def test_correct_message_for_missing_ticket_type(self):
        form = AddTicketForm({'ticket_type': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ticket_type'], [
                         u'This field is required.'])

    def test_correct_message_for_missing_priority(self):
        form = AddTicketForm({'priority': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['priority'], [
                         u'This field is required.'])

    def test_correct_message_for_missing_status(self):
        form = AddTicketForm({'status': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['status'], [
                         u'This field is required.'])

    def test_correct_error_message_for_missing_summary(self):
        form = AddTicketForm({'summary': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['summary'], [
                         u'This field is required.'])

    def test_correct_error_message_for_missing_description(self):
        form = AddTicketForm({'description': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['description'], [
                         u'This field is required.'])
