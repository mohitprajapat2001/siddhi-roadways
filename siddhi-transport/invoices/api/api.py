from rest_framework import viewsets
from invoices.models import Invoice, InvoiceDetail, Item
from invoices.api.serializers import (
    InvoiceSerializer,
    InvoiceDetailSerializer,
    ItemSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceDetailViewSet(viewsets.ModelViewSet):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
