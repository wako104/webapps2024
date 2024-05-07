# URL configuration for webapps2024 project.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('payapp.urls')),
    path('api/', include('conversion.urls'))
]
