from django.contrib import admin
from .models import User, Transaction, Request


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'currency', 'balance', 'is_superuser')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('sender', 'receiver', 'amount', 'created_at', 'successful')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
	list_display = ('requester', 'requestee', 'amount', 'created_at', 'fulfilled')

