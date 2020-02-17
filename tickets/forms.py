from django import forms
from .models import Ticket

class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('ticket_type', 'summary', 'description')