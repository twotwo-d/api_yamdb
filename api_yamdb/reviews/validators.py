from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if not (-9999 < value <= timezone.now().year):
        raise ValidationError('Некорректно указан год произведения!')
