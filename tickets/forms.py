from django import forms
from django.contrib.auth.models import User
from .models import Ticket, Comment

# ChoiceField choices
TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))
PRIORITIES = (('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'))
STATUSES = (('New', 'New'),  ('In Progress', 'In Progress'),
            ('Resolved', 'Resolved'), ('Cancelled', 'Cancelled'))


# ? not used
# class DateInput(forms.DateInput):
#     input_type = 'date'


class AddTicketForm(forms.ModelForm):
    ticket_type = forms.ChoiceField(
        choices=TICKET_TYPES, required=True, label='Ticket Type')
    priority = forms.ChoiceField(choices=PRIORITIES, required=True)
    status = forms.ChoiceField(choices=STATUSES, required=True)

    class Meta:
        model = Ticket
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Summary'}),
            'description': forms.Textarea(attrs={'placeholder': 'Add a description',
                                                 'rows': 4}),
        }
        fields = ('ticket_type', 'summary',
                  'description', 'priority',
                  'status', 'tags', 'screenshot')


class EditTicketForm(forms.ModelForm):
    # Same as Add except for AddTicketForm
    ticket_type = forms.ChoiceField(
        choices=TICKET_TYPES, required=True, label='Ticket Type')
    assigned_to = forms.ModelChoiceField(User.objects, label='Assign to')
    priority = forms.ChoiceField(choices=PRIORITIES, required=True)
    status = forms.ChoiceField(choices=STATUSES, required=True)

    class Meta:
        model = Ticket
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Summary'}),
            'description': forms.Textarea(attrs={'placeholder': 'Add a description', 'rows': 4}),
        }
        fields = ('ticket_type', 'summary',
                  'description', 'priority',
                  'status', 'tags', 'assigned_to', 'screenshot')


class AddCommentForm(forms.ModelForm):
    """Adds a comment"""
    class Meta:
        model = Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body': forms.Textarea(attrs={'placeholder': 'Leave a comment', 'rows': 3})
        }
        labels = {
            'comment_body': '',
        }
        error_messages = {
            'comment_body': {
                'required': '',
            }
        }
