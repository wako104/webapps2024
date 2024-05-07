from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import User, Transaction, Request


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'currency', 'password1', 'password2']
		widgets = {
			'currency': forms.RadioSelect(choices=User.CURRENCY)
		}
		first_name = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('username', css_class='form-group'),
				Column('email', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Row(
				Column('first_name', css_class='form-group'),
				Column('last_name', css_class='form-group'),
				css_class='row mb-3'
			),
			Row(
				Column('currency', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Row(
				'password1',
				'password2',
				css_class='form-row mb-3'
			),
			Submit('submit', 'Sign Up', css_class='btn btn-primary mt-3')
		)


class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			Row(
				Column('username', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Row(
				Column('password', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Submit('submit', 'Log In', css_class='btn btn-primary')
		)


class TransactionForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)

	class Meta:
		model = Transaction
		fields = ['receiver', 'amount']


class RequestForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)

	class Meta:
		model = Request
		fields = ['requestee', 'amount']

