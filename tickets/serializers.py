from rest_framework import serializers
from .models import Ticket
from django.contrib.auth.models import User


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('ticket_type', 'summary', 'description',
                  'priority', 'assigned_to', 'status', 'upvotes', 'created_date')
