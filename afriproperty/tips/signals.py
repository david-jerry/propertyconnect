import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from afriproperty.utils.unique_slug_generator import unique_slug_generator

from .models import Tip


@receiver(pre_save, sender=Tip)
def create_tip_slug(sender, instance, *args, **kwargs):
	if instance.title and not instance.slug:
		instance.slug = unique_slug_generator(instance)


@receiver(post_save, sender=Tip)
def create_pub_date_after_approved(sender, instance, *args, **kwargs):
	if instance.approved:
		instance.pub_date = datetime.date.today()


