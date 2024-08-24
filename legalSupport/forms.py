from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.models import User
from django import forms
        
class CreateUserForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        min_length=8)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password Again'}),
        min_length=8)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Enter your email'}))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'New Password'}), min_length=8)
    new_password2 = forms.CharField(label="Confirm New password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm New Password'}), min_length=8,
        help_text=password_validation.password_validators_help_text_html())
