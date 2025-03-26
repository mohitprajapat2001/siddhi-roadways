from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from django.db import models
from django.contrib.auth import get_user_model
from invoices.constants import InvoiceChoices
from cities_light.models import City
from random import randint


def generate_invoice_number():
    """Generate a unique invoice number with 'INV' prefix and 5-digit random number."""
    while True:
        unique_number = f"INV{randint(10000, 99999)}"
        if not Invoice.objects.filter(invoice_number=unique_number).exists():
            return unique_number


class PrefixedUUIDField(models.CharField):
    """Custom field to generate unique invoice numbers with 'INV' prefix."""

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 8
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        value = getattr(instance, self.attname)
        if not value:
            value = generate_invoice_number()
            setattr(instance, self.attname, value)
        return value


class Invoice(TimeStampedModel):
    invoice_number = PrefixedUUIDField(unique=True)
    truck_number = models.CharField(max_length=16, null=True, blank=True)
    to_pay = models.BooleanField(
        default=InvoiceChoices.NOT_PAID, choices=InvoiceChoices.STATUS_CHOICES
    )
    consignor = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="invoice_consignor"
    )
    consignee = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="invoice_consignee"
    )
    source = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="invoice_source"
    )
    destination = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="invoice_destination"
    )

    @property
    def grand_total(self):
        # TODO: update implementation wrong
        return sum([item.freight for item in self.details.items.all()])

    def __str__(self):
        return self.invoice_number


class Item(TitleDescriptionModel):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    @property
    def freight(self):
        return self.quantity * self.price

    class Meta:
        verbose_name_plural = "Items"
        ordering = ["title"]
