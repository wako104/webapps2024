from django.shortcuts import redirect
import requests

CURRENCY_SYMBOLS = {
	'GBP': '£',
	'USD': '$',
	'EUR': '€',
}


def get_currency_symbol(currency_code):
	return CURRENCY_SYMBOLS.get(currency_code, currency_code)


def convert_currency(currency1, currency2, amount):
	conversion = requests.get(f'http://localhost:8000/api/convert/{currency1}/{currency2}/{amount}/')
	return conversion.json().get('converted_amount', amount)


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('dashboard')
		return view_func(request, *args, **kwargs)
	return wrapper_func

