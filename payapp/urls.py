from django.urls import path
from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("register/", views.register_view, name="register"),
	path("login/", views.login_view, name="login"),
	path("dashboard/", views.dashboard_view, name="dashboard"),
	path("logout/", views.logout_view, name="logout"),
	path("send/", views.send_payment_view, name="send_payment"),
	path("request/", views.request_payment_view, name="request_payment"),
	path('accept_request/<int:pk>/', views.accept_request, name='accept_request'),
	path('reject_request/<int:pk>/', views.reject_request, name='reject_request')
]
