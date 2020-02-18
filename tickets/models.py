from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))

class Ticket(models.Model):
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES)
    summary = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='New')
    priority = models.CharField(max_length=50, default='Medium')
    # reporter = models.ForeignKey(User, default=None)
    description = models.TextField()
    def __str__(self):
        return self.summary
    class Meta:
        verbose_name_plural = "Tickets"
    # assignee = models.CharField(maximum_length=200)
    # tags = models.CharField(maximum_length=200)
    # attachments = models.CharField(maximum_length=200)
    # upvotes = models.IntegerField()