from django.db import models
from datetime import datetime

# Create your models here.
class Ticket(models.Model):
    ticket_type = models.CharField(max_length=50)
    summary = models.CharField(max_length=300)
    def __str__(self):
        return self.summary
    class Meta:
        verbose_name_plural = "Tickets"
    # raised_by = models.CharField(maximum_length=200)
    # created_date = models.DateTimeField(auto_now_add=True)
    # assigned_to = models.CharField(maximum_length=200)
    # priority = models.CharField(maximum_length=200)
    # status = models.CharField(maximum_length=200)
    # description = models.CharField(maximum_length=200)
    # tags = models.CharField(maximum_length=200)
    # attachments = models.CharField(maximum_length=200)
    # upvotes = models.IntegerField()