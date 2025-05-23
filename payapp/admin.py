from django.contrib import admin
from .models import User, Transaction, Request


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'currency', 'balance', 'is_superuser')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('sender', 'receiver', 'sender_amount', 'receiver_amount', 'created_at', 'successful')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
	list_display = ('requester', 'requestee', 'requestee_amount', 'requester_amount', 'created_at', 'fulfilled')

