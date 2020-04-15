from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords
import datetime


# Select Dropdown Options
TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))
PRIORITIES = (('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'))
STATUSES = (('New', 'New'),  ('In Progress', 'In Progress'),
            ('Resolved', 'Resolved'), ('Cancelled', 'Cancelled'))

# Ticket Model


class Ticket(models.Model):
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES)
    summary = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, default=None)
    status = models.CharField(max_length=50, default='New', choices=STATUSES)
    priority = models.CharField(
        max_length=50, default='Medium', choices=PRIORITIES)
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='submitted_by')
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assigned_to', default=1)
    description = models.TextField()
    tags = TaggableManager(blank=True)
    upvotes = models.IntegerField(default=0)
    screenshot = models.ImageField(
        upload_to='screenshots', null=True, default=None, blank=True)
    history = HistoricalRecords()

    def age(self):
        created_date_only = self.created_date.date()
        return int((datetime.date.today() - created_date_only).days)

    def days_to_resolve(self):
        if self.resolved_date:
            return int(
                (self.resolved_date.date() - self.created_date.date()).days
            )
        else:
            return None

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name_plural = "Tickets"


# Comment Model
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_body

    class Meta:
        verbose_name_plural = "Comments"
