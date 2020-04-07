from django.test import TestCase, Client
from accounts.models import User
from .models import Ticket, Comment


class TestViews(TestCase):
    def setUp(self):
        # Every test needs access to this logged in user
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_create_a_ticket_with_summary_and_description(self):
        # Create Ticket (TicketID = 1)
        ticket = Ticket(ticket_type="Bug",
                        summary='Test Summary',
                        description='Test Description',
                        status='New',
                        priority='Low',
                        submitted_by=self.user,
                        assigned_to=self.user
                        )
        ticket.save()
        self.assertEqual(ticket.summary, 'Test Summary')
        self.assertEqual(ticket.description, 'Test Description')

    def test_add_a_comment(self):
        # Create Ticket (TicketID = 1)
        ticket = Ticket(ticket_type="Bug",
                        summary='Test Summary',
                        description='Test Description',
                        status='New',
                        priority='Low',
                        submitted_by=self.user,
                        assigned_to=self.user
                        )
        ticket.save()
        comment = Comment(ticket=ticket, user=self.user,
                          comment_body='Test Comment')
        comment.save()
        comment = Comment.objects.get(pk=1)
        self.assertEqual(str(comment), comment.comment_body)
