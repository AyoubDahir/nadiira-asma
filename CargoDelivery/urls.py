import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('apps.userprofile.urls')),
    path('company/', include('apps.company.urls')),
    path('', include('apps.main.urls')),
]
