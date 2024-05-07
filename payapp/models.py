from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	CURRENCY = [
		('GBP', 'Great British Pound'),
		('EUR', 'Euro'),
		('USD', 'US Dollar')
	]
	first_name = models.CharField(max_length=30, blank=False, null=False)
	last_name = models.CharField(max_length=30, blank=False, null=False)
	email = models.EmailField(unique=True)
	currency = models.CharField(max_length=3, choices=CURRENCY)
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def __str__(self):
		return f"{self.username} ({self.email})"


class Transaction(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	successful = models.BooleanField(default=True)

	def __str__(self):
		return f"Transaction from {self.sender} to {self.receiver}: {self.amount}"


class Request(models.Model):
	requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_payments')
	requestee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_requests_received')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	fulfilled = models.BooleanField(default=False)

	def __str__(self):
		return f"Payment request from {self.requester} to {self.requestee}: {self.amount}"
