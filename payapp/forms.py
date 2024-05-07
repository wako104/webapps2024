from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Transaction, Request


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'currency', 'password1', 'password2']


class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['receiver', 'amount']


class RequestForm(forms.ModelForm):
	class Meta:
		model = Request
		fields = ['requestee', 'amount']

