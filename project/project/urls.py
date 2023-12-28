# project/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),  # Include app URLs
    # ... other included app URLs
]
