from django.contrib import admin
from django.urls import path, include
from api.views import health, spa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("health/", health),
    path("", spa),
]
