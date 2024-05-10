from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.db import transaction
import requests

from .models import Transaction, Request, User
from .forms import UserRegistrationForm, TransactionForm, RequestForm, UserLoginForm
from .utils import get_currency_symbol, unauthenticated_user, convert_currency


def home(request):
	return render(request, "home.html")


def initial_balance(currency):
	amount = 500
	conversion = requests.get(f'https://localhost:8000/api/convert/GBP/{currency}/{amount}/', verify=False)
	return conversion.json().get('converted_amount', amount)


@unauthenticated_user
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


@unauthenticated_user
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
	sent_transactions = Transaction.objects.filter(sender=request.user)
	received_transactions = Transaction.objects.filter(receiver=request.user)
	sent_requests = Request.objects.filter(requester=request.user)
	received_requests = Request.objects.filter(requestee=request.user)
	currency_symbol = get_currency_symbol(request.user.currency)
	return render(request, 'dashboard.html', {
		'sent_transactions': sent_transactions,
		'received_transactions': received_transactions,
		'sent_requests': sent_requests,
		'received_requests': received_requests,
		'currency_symbol': currency_symbol
	})


@csrf_protect
@login_required
def send_payment_view(request):
	if request.method == 'POST':
		form = TransactionForm(request.POST)
		if form.is_valid():
			receiver_username = form.cleaned_data.get('receiver_username')
			sender_amount = form.cleaned_data.get('sender_amount')
			try:
				receiver = User.objects.get(username=receiver_username)
				sender_currency = request.user.currency
				receiver_currency = receiver.currency
				receiver_amount = convert_currency(sender_currency, receiver_currency, sender_amount)

				if request.user.balance >= sender_amount:
					with transaction.atomic():
						request.user.balance -= sender_amount
						receiver.balance += receiver_amount
						request.user.save()
						receiver.save()

						Transaction.objects.create(
							sender=request.user,
							receiver=receiver,
							sender_amount=sender_amount,
							receiver_amount=receiver_amount
						)
					messages.success(request, 'Payment Successful.')
					return redirect('dashboard')
				else:
					messages.error(request, 'Insufficient Funds.')
			except User.DoesNotExist:
				form.add_error('receiver_username', 'User Not Found')
	else:
		form = TransactionForm()
	return render(request, 'send_payment.html', {'form': form})


@csrf_protect
@login_required
def request_payment_view(request):
	if request.method == 'POST':
		form = RequestForm(request.POST)
		if form.is_valid():
			requestee_username = form.cleaned_data.get('requestee_username')
			requester_amount = form.cleaned_data.get('requester_amount')
			try:
				requestee = User.objects.get(username=requestee_username)
				requester_currency = request.user.currency
				requestee_currency = requestee.currency
				requestee_amount = convert_currency(requester_currency, requestee_currency, requester_amount)

				payment_request = form.save(commit=False)
				payment_request.requester = request.user
				payment_request.requestee = requestee
				payment_request.requester_amount = requester_amount
				payment_request.requestee_amount = requestee_amount
				payment_request.save()
				messages.success(request, 'Payment Request Sent.')
				return redirect('dashboard')
			except User.DoesNotExist:
				form.add_error('requestee_username', 'User not found')
	else:
		form = RequestForm()
	return render(request, 'request_payment.html', {'form': form})


@login_required
def accept_request(request, pk):
	try:
		payment_request = Request.objects.get(pk=pk, requestee=request.user)
		if payment_request.status == 'PENDING':
			with transaction.atomic():
				requestee_amount = payment_request.requestee_amount
				requester_amount = payment_request.requester_amount

				if request.user.balance >= requestee_amount:
					request.user.balance -= requestee_amount
					payment_request.requester.balance += requester_amount
					request.user.save()
					payment_request.requester.save()

					Transaction.objects.create(
						sender=request.user,
						receiver=payment_request.requester,
						sender_amount=requestee_amount,
						receiver_amount=requester_amount
					)

					payment_request.status = 'ACCEPTED'
					payment_request.save()
					messages.success(request, 'Payment request accepted')
				else:
					messages.error(request, 'Insufficient funds')
		else:
			messages.info(request, 'Payment request is already processed!')
	except Request.DoesNotExist:
		messages.error(request, 'Payment request not found.')
	return redirect('dashboard')


@login_required
def reject_request(request, pk):
	try:
		payment_request = Request.objects.get(pk=pk, requestee=request.user)
		if payment_request.status == 'PENDING':
			payment_request.status = 'REJECTED'
			payment_request.save()
			messages.success(request, 'Payment request rejected!')
		else:
			messages.info(request, 'Payment request is already processed!')
	except Request.DoesNotExist:
		messages.error(request, 'Payment request not found.')
	return redirect('dashboard')