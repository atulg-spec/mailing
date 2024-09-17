from django import forms
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()

class Email_account(forms.ModelForm):
    class Meta:
        model = EmailAccounts
        fields = ['email', 'apppassword']


class Client_email(forms.ModelForm):
    class Meta:
        model = EmailAudience
        fields = ['email']

class EmailClientDataForm(forms.ModelForm):
    class Meta:
        model = EmailClientData
        fields = ['csv_file']

