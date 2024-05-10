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
	receiver_username = forms.CharField(max_length=150, label="Payee", required=True)

	class Meta:
		model = Transaction
		fields = ['receiver_username', 'sender_amount']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['sender_amount'].widget.attrs.update({'placeholder': f"{currency_symbol}"})
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			Row(
				Column('receiver_username', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Row(
				Column('sender_amount', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Submit('submit', 'Send Payment', css_class='btn btn-primary')
		)


class RequestForm(forms.ModelForm):
	requestee_username = forms.CharField(max_length=150, label="Requestee", required=True)

	class Meta:
		model = Request
		fields = ['requestee_username', 'requester_amount']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
			Row(
				Column('requestee_username', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Row(
				Column('requester_amount', css_class='form-group'),
				css_class='form-row mb-3'
			),
			Submit('submit', 'Request Payment', css_class='btn btn-primary')
		)
