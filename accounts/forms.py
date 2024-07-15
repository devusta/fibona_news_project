from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(label=_('Birth date'), widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(label=_('Phone number'), widget=forms.TextInput(attrs={'type': 'number'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'phone_number')
        labels = {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'phone_number')
        labels = {
            'username': _('Username'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'birth_date': _('Birth date'),
            'phone_number': _('Phone number'),
        }


class CustomProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'address')
        labels = {
            'photo': _('Photo'),
            'address': _('Address'),
        }


# # CustomUserCreationForm with ModelForm
# class CustomUserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
#     password2 = forms.CharField(label=_('Password confirm'), widget=forms.PasswordInput)
#     birth_date = forms.DateField(label=_('Birth date'), widget=forms.DateInput(attrs={'type': 'date'}))
#
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'phone_number')
#
#     def clean_password2(self):
#         data = self.cleaned_data
#         if data['password1'] and data['password2'] and data['password1'] != data['password2']:
#             raise ValidationError('Passwords must match!')
#         return data['password2']


# # Custom LoginForm with Form
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


# # Overwritten LoginForm with AuthenticationForm
# class CustomLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomLoginForm, self).__init__(*args, **kwargs)
#
#     error_messages = {
#         "invalid_login": _(
#             "Iltimos, foydalanuvchi nomi va parolni to'g'ri kiriting. "
#             "E'tibor bering bosh va kichik harflar farqlanadi."
#         ),
#         "inactive": _("This account is inactive."),
#     }



