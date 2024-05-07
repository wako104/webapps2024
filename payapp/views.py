from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
import requests

from .models import User, Transaction, Request
from .forms import UserRegistrationForm, TransactionForm, RequestForm, UserLoginForm


def home(request):
	return render(request, "home.html")


def initial_balance(currency):
	amount = 500
	conversion = requests.get(f'http://localhost:8000/api/convert/GBP/{currency}/{amount}/')
	return conversion.json().get('converted_amount', amount)


def register_view(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			# create user model and add form data to it
			user = form.save(commit=False)
			user.balance = initial_balance(user.currency)
			user.save()
			login(request, user)
			return redirect('dashboard')
	else:
		form = UserRegistrationForm()
	return render(request, 'register.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		form = UserLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('dashboard')
	else:
		form = UserLoginForm()
	return render(request, 'login.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('home')


@login_required
def dashboard_view(request):
	transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
	payment_requests = Request.objects.filter(requestee=request.user, fulfilled=False)
	return render(request, 'dashboard.html', {'transactions': transactions, 'requests': payment_requests})


@login_required
def send_payment_view(request):
	if request.method == 'POST':
		form = TransactionForm(request.POST)
		if form.is_valid():
			receiver = form.cleaned_data['receiver']
			amount = form.cleaned_data['amount']
			if request.user.balance >= amount:
				with transaction.atomic():
					request.user.balance -= amount
					receiver.balance += amount
					request.user.save()
					receiver.save()
					Transaction.objects.create(sender=request.user, receiver=receiver, amount=amount)
				messages.success(request, 'Payment Successful.')
				return redirect('dashboard')
			else:
				messages.error(request, 'Insufficient Funds.')
	else:
		form = TransactionForm()
	return render(request, 'send_payment.html', {'form': form})


@login_required
def request_payment_view(request):
	if request.method == 'POST':
		form = RequestForm(request.POST)
		if form.is_valid():
			payment_request = form.save(commit=False)
			payment_request.requester = request.user
			payment_request.save()
			messages.success(request, 'Payment Request Sent.')
			return redirect
	else:
		form = TransactionForm()
	return render(request, 'request_payment.html', {'form': form})
