from django import forms
from .models import Ticket

TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))


class AddTicketForm(forms.ModelForm):
    ticket_type = forms.ChoiceField(choices=TICKET_TYPES, required=True)
    # tags = forms.CharField(required=False)

    class Meta:
        model = Ticket
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Summary'}),
            'description': forms.Textarea(attrs={'placeholder': 'Further Details'}),
        }
        fields = ('ticket_type', 'summary', 'description', 'tags')
