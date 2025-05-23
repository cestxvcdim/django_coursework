from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm, \
    AuthenticationForm

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'country', 'avatar')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User


class UserPasswordSetForm(StyleFormMixin, SetPasswordForm):
    class Meta:
        model = User


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User


class UserManagerForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('is_active', )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
