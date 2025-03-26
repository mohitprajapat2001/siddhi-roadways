from django.utils.translation import gettext_lazy as _


class InvoiceChoices:
    PAID = 1
    NOT_PAID = 0

    STATUS_CHOICES = [
        (PAID, _("Paid")),
        (NOT_PAID, _("Not Paid")),
    ]
