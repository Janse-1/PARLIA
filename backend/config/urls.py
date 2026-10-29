from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.learning.urls')),
    path('api/v1/', include('apps.progress.urls')),
    path('api/v1/', include('apps.activities.urls')),
]
