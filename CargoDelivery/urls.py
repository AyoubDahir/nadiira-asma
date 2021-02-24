from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('apps.userprofile.urls')),
    path('company/', include('apps.company.urls')),
    path('', include('apps.main.urls')),
]
