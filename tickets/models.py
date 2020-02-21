from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords

# Create your models here.

TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))


class Ticket(models.Model):
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES)
    summary = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='New')
    priority = models.CharField(max_length=50, default='Medium')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=200, default='Unassigned')
    description = models.TextField()
    tags = TaggableManager(blank=True)
    upvotes = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name_plural = "Tickets"
    # attachments = models.CharField(maximum_length=200)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_body

    class Meta:
        verbose_name_plural = "Comments"


# class ChangeHistory(models.Model):
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
    # field?
