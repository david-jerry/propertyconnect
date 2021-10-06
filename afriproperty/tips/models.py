from __future__ import absolute_import

# development system imports
import os
import random
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal

import readtime
from comment.models import Comment
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags import humanize
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
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
    IntegerField,
    ManyToManyField,
    OneToOneField,
    PositiveIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.db.models.fields import FloatField
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

User = settings.AUTH_USER_MODEL

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
char_regex = RegexValidator(regex=r'^[A-Za-z]*$', message="Field must be only alphabets: A-Z or a-z")

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def tip_images(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "tip-photo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

def tip_video(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "tip-video/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

# Create your models here.
class Tip(TimeStampedModel):
    BLOG = "Blog Post"
    TIP = "Tip"
    NEWS = "News Info"

    TIP_TYPE = (
        (BLOG , "Blog Post"),
        (TIP , "Tip"),
        (NEWS , "News Info"),
    )

    tip_author = ForeignKey(User, on_delete=CASCADE, related_name="tipauthor")
    title = CharField(_("Tip Title"), null=True, blank=False, max_length=500)
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    tip_type = CharField(_("Tip Type"), max_length=11, choices=TIP_TYPE, default=TIP, null=True, blank=True)
    tip_content = HTMLField()
    comments =  GenericRelation(Comment)

    published = BooleanField(default=False)
    approved = BooleanField(default=False)
    featured = BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def get_related_tip(self):
        return Tip.objects.filter(tip_agent=self.tip_author, tip_type=self.tip_type)[:10]

    def get_related_tip_by_author(self):
        return Tip.objects.filter(tip_agent=self.tip_author)[:10]

    def get_image_url(self):
        img = self.tipimage.first()
        if img:
            return img.image.url
        return None

    def get_video_url(self):
        img = self.tipvideo.first()
        if img:
            return img.video.url
        return None

    def get_all_images(self):
        return self.tipimage.all()

    def readtime(self):
        return str(readtime.of_test(self.tip_content))



    class Meta:
        managed = True
        verbose_name = "Tip"
        verbose_name_plural = "Tips"
        ordering = ["-created", "title"]

    def get_absolute_url(self):
        """Get url for blog's detail view.

        Returns:
            str: URL for blog detail.

        """
        return reverse("tips:detail", kwargs={"slug": self.slug})


    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"


class TipImageFile(TimeStampedModel):
    tip = ForeignKey(Tip, on_delete=CASCADE, related_name="tipimage")
    image = FileField(upload_to=tip_images)

    def __str__(self):
        return f"{self.tip.title} Image"

class TipVideoFile(TimeStampedModel):
    tip = ForeignKey(Tip, on_delete=CASCADE, related_name="tipvideo")
    video = FileField(upload_to=tip_video, help_text="Your video should be 40Seconds Long, 20MB in size max")

    def __str__(self):
        return f"{self.tip.title} Video"

