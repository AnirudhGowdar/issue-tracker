from django.forms import ModelForm
from home.models import Project
from django import forms

attrs_dict = {'class': 'required form-control'}


class CreateProjectForm(ModelForm):
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
        model = Project
        fields = [
            'title', 'description'
        ]
