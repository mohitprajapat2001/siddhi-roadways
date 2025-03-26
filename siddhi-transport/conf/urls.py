from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts.api.api import CityViewSet, UserViewSet, LoginApiView
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register("cities", CityViewSet)
router.register("users", UserViewSet)


urlpatterns = [
    path("", RedirectView.as_view(url="api/")),
    path("admin/", admin.site.urls),
    path("api/login/", LoginApiView.as_view()),
    path("api/", include("invoices.urls")),
    path("api/", include(router.urls)),
]
