from django.db import models
from datetime import datetime

# Create your models here.
class Ticket(models.Model):
    ticket_type = models.CharField(max_length=10)
    summary = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='New')
    priority = models.CharField(max_length=50, default='Medium')
    description = models.TextField()
    def __str__(self):
        return self.summary
    class Meta:
        verbose_name_plural = "Tickets"
    # reporter = models.CharField(maximum_length=200)
    # assignee = models.CharField(maximum_length=200)
    # tags = models.CharField(maximum_length=200)
    # attachments = models.CharField(maximum_length=200)
    # upvotes = models.IntegerField()