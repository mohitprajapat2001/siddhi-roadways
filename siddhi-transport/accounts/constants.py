from django.utils.translation import gettext_lazy as _


class FormValdationMessages:
    REQUIRED_FIELDS = _("All fields are required")
    CONSIGNEE_CONSIGNOR_SAME = _("Consignee cannot be the same as Consignor")
    USER_NOT_FOUND = _("User not found")
    CITY_NOT_FOUND = _("City not found")
    INVALID_CREDENTIALS = _("Invalid username or password")
