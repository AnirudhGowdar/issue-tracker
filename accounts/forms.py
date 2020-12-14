from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm

attrs_dict = {'class': 'required form-control'}


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs=attrs_dict),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Invalid characters in first name',
                code='invalid_first_name'
            ),
        ]
    )

    last_name = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs=attrs_dict),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Invalid characters in last name',
                code='invalid_last_name'
            ),
        ]
    )

    username = forms.CharField(
        max_length=20,
        min_length=6,
        widget=forms.TextInput(attrs=attrs_dict),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Username must be Alphanumeric',
                code='invalid_username'
            ),
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs=dict(attrs_dict, maxlength=75)),
        label='Email'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label='Confirm Password'
    )

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(
                'A user with that username already exists.'
            )
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(
                'A user with that email already exists.'
            )
        return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    'The two password fields do not match.'
                )
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'password1', 'password2'
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs=attrs_dict),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label='Password',
        error_messages={
            'incomplete': 'Please enter a valid password.'
        }
    )
class EditProfileForm(ModelForm):
    
    first_name = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs=attrs_dict),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Invalid characters in first name',
                code='invalid_first_name'
            ),
        ]
    )

    last_name = forms.CharField(
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs=attrs_dict),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]*$',
                message='Invalid characters in last name',
                code='invalid_last_name'
            ),
        ]
    )

    username = forms.CharField(
        max_length=20,
        min_length=6,
        widget=forms.TextInput(attrs=attrs_dict),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Username must be Alphanumeric',
                code='invalid_username'
            ),
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs=dict(attrs_dict, maxlength=75)),
        label='Email'
    )
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email'
        ]
