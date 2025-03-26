from rest_framework import viewsets
from invoices.models import Invoice, Item
from invoices.api.serializers import (
    InvoiceSerializer,
    ItemSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
