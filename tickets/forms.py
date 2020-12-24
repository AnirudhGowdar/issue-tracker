from django.contrib.auth.models import User
from django.forms import ModelForm
from home.models import Project, Ticket, TicketPriority, TicketStatus, TicketType
from django import forms

attrs_dict = {'class': 'required form-control'}


class CreateTicketForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'})
        )
        self.fields['ticket_type'] = forms.ModelChoiceField(
            queryset=TicketType.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'})
        )

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
            'title', 'description', 'project', 'ticket_type', 'attachment'
        ]


class EditTicketForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'}
            )
        )
        self.fields['ticket_type'] = forms.ModelChoiceField(
            queryset=TicketType.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'}
            )
        )
        self.fields['ticket_priority'] = forms.ModelChoiceField(
            queryset=TicketPriority.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'}
            )
        )
        self.fields['ticket_status'] = forms.ModelChoiceField(
            queryset=TicketStatus.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'}
            )
        )

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
            'title', 'description', 'project', 'ticket_type', 'attachment'
        ]


class AssignDeveloperForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignDeveloperForm, self).__init__(*args, **kwargs)
        print(self.instance)
        self.fields['ticket_priority'] = forms.ModelChoiceField(
            queryset=TicketPriority.objects.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'}
            )
        )
        self.fields['assigned_to'] = forms.ModelChoiceField(
            queryset=self.instance.project.developers.all(),
            widget=forms.Select(
                attrs={'class': 'required form-control custom-select'}
            )
        )

    class Meta:
        model = Ticket
        fields = [
            'ticket_priority', 'assigned_to'
        ]
