from django import forms
from .models import Ticket

TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))

class AddTicketForm(forms.ModelForm):
    ticket_type = forms.ChoiceField(choices=TICKET_TYPES, required=True)
    class Meta:
        model = Ticket
        fields = ('ticket_type', 'summary', 'description')