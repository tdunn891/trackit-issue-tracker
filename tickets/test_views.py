from django.shortcuts import get_object_or_404
from django.test import TestCase
from accounts.models import User, Profile
from .models import Ticket


class TestViews(TestCase):
    def setUp(self):
        # Every test needs access to this logged in user
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

        # Create Ticket (TicketID = 1)
        Ticket.objects.create(ticket_type="Bug",
                              summary='Test Summary',
                              description='Test Description',
                              status='New',
                              priority='Low',
                              submitted_by=self.user,
                              assigned_to=self.user
                              )

    def test_get_index_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "index.html")

    def test_get_view_tickets_page(self):
        page = self.client.get("/tickets/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "tickets.html")

    def test_add_ticket_page(self):
        page = self.client.get("/tickets/add_ticket/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "add_ticket.html")

    def test_dashboard_page(self):
        page = self.client.get("/tickets/dashboard/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "dashboard.html")

    def test_kanban_page_as_pro_user(self):
        # Set user to Pro User
        self.user.profile.is_pro_user = True
        self.user.profile.save()
        page = self.client.get("/tickets/kanban/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "kanban.html")

    def test_kanban_page_as_basic_user(self):
        # Set user to Basic
        self.user.profile.is_pro_user = False
        self.user.profile.save()
        page = self.client.get("/tickets/kanban/")
        # Redirects to Checkout page
        self.assertRedirects(page, "/checkout/")

    def test_edit_ticket_page(self):
        page = self.client.get("/tickets/edit_ticket/1/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "edit_ticket.html")

    def test_view_ticket_page(self):
        page = self.client.get("/tickets/1/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "view_ticket.html")

    def test_get_view_page_for_ticket_that_does_not_exist(self):
        page = self.client.get("tickets/1000/")
        self.assertEqual(page.status_code, 404)

    def test_get_edit_page_for_ticket_that_does_not_exist(self):
        page = self.client.get("tickets/edit/1000/")
        self.assertEqual(page.status_code, 404)

    def test_upvote_for_ticket_that_does_not_exist(self):
        page = self.client.get("tickets/upvote/1000/")
        self.assertEqual(page.status_code, 404)

    def test_change_status_for_ticket_that_does_not_exist(self):
        page = self.client.get("tickets/change_status/1000/Cancelled")
        self.assertEqual(page.status_code, 404)

    # POSTs
    def test_post_create_a_ticket(self):
        new_ticket = {"ticket_type": "Bug",
                      "summary": 'Test Summary 2',
                      "description": 'Test Description',
                      "status": 'New',
                      "priority": 'Low',
                      "submitted_by": self.user,
                      "assigned_to": self.user
                      }
        response = self.client.post("/tickets/add_ticket/", new_ticket)
        ticket = get_object_or_404(Ticket, pk=2)
        self.assertEqual(ticket.summary, "Test Summary 2")

    def test_post_upvote_a_ticket(self):
        response = self.client.post(
            "/tickets/upvote/1/")
        ticket = get_object_or_404(Ticket, pk=1)
        self.assertEqual(ticket.upvotes, 1)

    def test_change_ticket_status(self):
        response = self.client.post(
            "/tickets/change_status/1/Resolved/")
        ticket = get_object_or_404(Ticket, pk=1)
        self.assertEqual(ticket.status, "Resolved")
