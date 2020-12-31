from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
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


class EditProjectForm(ModelForm):

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
            'title', 'description', 'archived'
        ]


class AssignUsersForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignUsersForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(groups__name='developers')
        devs = self.instance.developers.all()
        users_available = users.exclude(id__in=devs)
        self.fields['developers'] = forms.ModelMultipleChoiceField(
            queryset=users_available,
            label='Add developers',
            widget=forms.SelectMultiple(
                attrs={'class': 'required form-control custom-select'}
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['developers'] = cleaned_data['developers'] | self.instance.developers.all()
        print(cleaned_data['developers'])
        return cleaned_data

    class Meta:
        model = Project
        fields = [
            'developers'
        ]


class RemoveUsersForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RemoveUsersForm, self).__init__(*args, **kwargs)
        self.fields['developers'] = forms.ModelMultipleChoiceField(
            queryset=self.instance.developers.all(),
            label='Remove developers',
            widget=forms.SelectMultiple(
                attrs={'class': 'required form-control custom-select'}
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['developers'] = self.instance.developers.all().exclude(
            id__in=cleaned_data['developers']
        )
        print(cleaned_data['developers'])
        return cleaned_data

    class Meta:
        model = Project
        fields = [
            'developers'
        ]
