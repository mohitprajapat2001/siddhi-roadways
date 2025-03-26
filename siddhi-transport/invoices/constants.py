from django.utils.translation import gettext_lazy as _


class InvoiceChoices:
    PAID = 1
    NOT_PAID = 0

    STATUS_CHOICES = [
        (PAID, _("Paid")),
        (NOT_PAID, _("Not Paid")),
    ]


class ValidationErrorMessages:
    CONSIGNOR_NOT_EMPTY = _("Consignor cannot be empty.")
    CONSIGNEE_NOT_EMPTY = _("Consignee cannot be empty.")
    SOURCE_NOT_EMPTY = _("Source cannot be empty.")
    DESTINATION_NOT_EMPTY = _("Destination cannot be empty.")
    CONSIGNOR_CONSIGNEE_NOT_SAME = _("Consignee and Consignor cannot be the same.")
