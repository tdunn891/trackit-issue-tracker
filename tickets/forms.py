from django import forms
from .models import Ticket, Comment

TICKET_TYPES = (('Bug', 'Bug'), ('Feature', 'Feature'))


class AddTicketForm(forms.ModelForm):
    ticket_type = forms.ChoiceField(choices=TICKET_TYPES, required=True)
    # tags = forms.CharField(required=False)

    class Meta:
        model = Ticket
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Summary'}),
            'description': forms.Textarea(attrs={'placeholder': 'Details', 'rows': 4}),
            # 'tags': forms.TextInput(attrs={'placeholder': 'eg. Project Alpha, Testing'}),
        }
        fields = ('ticket_type', 'summary', 'description', 'tags')


class AddCommentForm(forms.ModelForm):
    """Adds a comment"""
    class Meta:
        model = Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body': forms.Textarea(attrs={'placeholder': 'Leave a comment', 'rows': 3})
        }
        labels = {
            # 'comment_body': ('test'),
            'comment_body': '',
        }
        error_messages = {
            'comment_body': {
                'required': '',
            }
        }
