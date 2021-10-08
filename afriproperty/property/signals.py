from datetime import timezone

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from afriproperty.utils.unique_slug_generator import unique_slug_generator

from .models import Property


@receiver(pre_save, sender=Property)
def create_property_slug(sender, instance, *args, **kwargs):
	if instance.title and not instance.slug:
		instance.slug = unique_slug_generator(instance)


