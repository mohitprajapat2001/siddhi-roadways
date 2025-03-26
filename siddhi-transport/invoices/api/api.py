from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from invoices.models import Invoice, Item
from invoices.api.serializers import (
    InvoiceSerializer,
    ItemSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)
