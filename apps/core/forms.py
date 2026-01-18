from django import forms
from django.core.exceptions import ValidationError


class TolerantDateField(forms.DateField):
    """A tolerant date field for not valid input date."""

    def to_python(self, value):
        """Convert the input to a Python object.

        If `value` is a valid date, return the corresponding date object.
        Otherwise, return a null string.

        """
        try:
            return super().to_python(value)
        except ValidationError:
            return ""
