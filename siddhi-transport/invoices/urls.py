from django.urls import path, include
from rest_framework import routers
from invoices.api.api import InvoiceViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register("invoices", InvoiceViewSet)
router.register("items", ItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
