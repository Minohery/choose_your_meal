from django import forms
from choice.models import User
from django.contrib.auth.password_validation import password_validators_help_text_html

class LoginForm(forms.Form):
    Username=forms.CharField(max_length=50)
    Password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username', 'password']

class ConfirmForm(forms.Form):
    code=forms.IntegerField()

class ChangeForm(forms.Form):
    Username=forms.CharField(max_length=50)
