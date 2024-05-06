from django.urls import path
from . import views

urlpatterns = [
	path('convert/<str:from_currency>/<str:to_currency>/<str:amount>/', views.convert_currency)
]

