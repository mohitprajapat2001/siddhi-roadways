from rest_framework import serializers
from invoices.models import Invoice, Item
from siddhi_transport.api.serializers import UserSerializer, CitySerializer
from django.contrib.auth import get_user_model
from cities_light.models import City

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "title", "description", "quantity", "price", "freight")

    def create(self, validated_data):
        invoice_id = self.initial_data.get("invoice_id")
        if not invoice_id:
            raise serializers.ValidationError({"error": "Invoice id is required field"})
        validated_data["invoice_id"] = invoice_id
        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    consignor = UserSerializer(read_only=True)
    consignee = UserSerializer(read_only=True)
    source = CitySerializer(read_only=True)
    destination = CitySerializer(read_only=True)
    items = ItemSerializer(read_only=True, many=True)

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
            "items",
        )
        extra_kwargs = {"invoice_number": {"read_only": True}}

    def validate(self, attrs):
        if self.initial_data.get("consignee") == self.initial_data.get("consignor"):
            raise serializers.ValidationError(
                "Consignee and Consignor cannot be the same."
            )
        try:
            User.objects.get(id=self.initial_data.get("consignee"))
            User.objects.get(id=self.initial_data.get("consignor"))
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid consignee or consignor.")
        try:
            City.objects.get(id=self.initial_data.get("source"))
            City.objects.get(id=self.initial_data.get("destination"))
        except City.DoesNotExist:
            raise serializers.ValidationError("Invalid source or destination.")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["consignee_id"] = self.initial_data["consignee"]
        validated_data["consignor_id"] = self.initial_data["consignor"]
        validated_data["source_id"] = self.initial_data["source"]
        validated_data["destination_id"] = self.initial_data["destination"]
        return super().create(validated_data)
