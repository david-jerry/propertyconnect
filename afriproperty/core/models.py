import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    OneToOneField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"
ABC_REGEX = "^[A-Za-z]*$"

# Create your models here.
class EmailSubscribe(TimeStampedModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = EmailField(_("Email Please"), blank=True, null=True)
    subscribed = BooleanField(default=True)

    def __str__(self):
        return f"{self.email} just subscribed to the mailing list"

    class Meta:
        managed = True
        verbose_name = "Email Subscriber"
        verbose_name_plural = "Email Subscribers"
        ordering = ["-created"]
