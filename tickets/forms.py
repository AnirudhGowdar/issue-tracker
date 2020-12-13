from django.forms import ModelForm
from home.models import Project, Ticket
from django import forms

attrs_dict = {'class': 'required form-control'}


class CreateTicketForm(ModelForm):
    title = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs=attrs_dict),

    )
    description = forms.CharField(
        widget=forms.Textarea(attrs=attrs_dict),
        label='description',
    )

    class Meta:
        model = Ticket
        fields = [
            'title', 'description', 'project_id', 'ticket_type',
        ]


class EditTicketForm(ModelForm):
    title = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs=attrs_dict),

    )
    description = forms.CharField(
        widget=forms.Textarea(attrs=attrs_dict),
        label='description',
    )

    class Meta:
        model = Ticket
        fields = [
            'title', 'description', 'project_id', 'ticket_type', 'ticket_priority', 'ticket_status'
        ]
