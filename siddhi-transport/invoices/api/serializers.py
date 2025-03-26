from rest_framework import serializers
from invoices.models import Invoice, Item, InvoiceDetail


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "title", "description", "weight", "price", "freight")


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "id",
            "invoice_number",
            "truck_number",
            "to_pay",
            "consignor",
            "consignee",
            "source",
            "destination",
        )


class InvoiceDetailSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()
    items = ItemSerializer(many=True)

    class Meta:
        model = InvoiceDetail
        fields = (
            "id",
            "invoice",
            "items",
        )
