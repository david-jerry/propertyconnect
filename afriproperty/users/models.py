from __future__ import absolute_import

# development system imports
import os
import random

from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags import humanize
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    GenericIPAddressField,
    OneToOneField,
    SlugField,
    URLField,
)
from django.db.models.fields import FloatField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
char_regex = RegexValidator(regex=r'^[A-Za-z]*$', message="Field must be only alphabets: A-Z or a-z")

class Banks(TimeStampedModel):
    title = CharField(_('Bank Name'), null=True, blank=True, max_length=500, unique=True)
    country = CharField(_('Bank Country'), null=True, blank=True, max_length=500)
    currency = CharField(_('Bank currency'), null=True, blank=True, max_length=3)
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    bank_code = CharField(_('Bank Code'), max_length=5, blank=True, null=True, unique=False)
    bank_id = CharField(_('Bank ID'), max_length=5, blank=True, null=True)

    def __str__(self):
        return self.title



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def profile_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "profile-photo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

def company_logo(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "company-logo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


class User(AbstractUser):
    """Default user for afriproperty."""
    INDIVIDUAL = "Individual [Searching for property]"
    PROPERTY_OWNER = "Property Owner"
    ESTATE_AGENT = "Estate Agent"
    PROPERTY_DEVELOPER = "Property Developers/Management Company"

    ACCOUNT_TYPE = (
        (INDIVIDUAL, "Individual [Searching for property]"),
        (PROPERTY_OWNER, "Property Owner"),
        (ESTATE_AGENT, "Estate Agent"),
        (PROPERTY_DEVELOPER, "Property Developer"),
    )

    #: First and last name do not cover name patterns around the globe
    phone_number = CharField(_("Phone Number"), blank=False, validators=[phone_regex], null=True, max_length=16)
    postcode = CharField(_("Postcode (Optional)"), blank=True, null=True, max_length=8)
    image = ResizedImageField(size=[300, 300], quality=75, crop=['middle', 'center'], upload_to=profile_image, force_format='JPEG', null=True, help_text="image size: 300x300")
    account_type = CharField(_("Account Type"), max_length=50, choices=ACCOUNT_TYPE, default="Individual [Searching for property]", null=True)
    facebook = URLField(_("Facebook Profile"), unique=True, blank=True, null=True, help_text="https://www.facebook.com/username/")
    linkedin = URLField(_("Linkedin Profile"), unique=True, blank=True, null=True, help_text="https://www.linkedin.com/in/username/")
    instagram = URLField(_("Instagram Profile"), unique=True, blank=True, null=True, help_text="https://www.google.com/profilename/")
    accept_terms = BooleanField(default=False)
    has_testified = BooleanField(default=False)

    # user initials
    def initials(self):
        fname = self.first_name[0].upper()
        lname = self.last_name[0].upper()
        return f"{fname} {lname}"

    @property
    def fullname(self):
        if self.first_name and self.last_name:
            fullname = f"{self.first_name} {self.last_name}"
        else:
            fullname = f"{self.username}"
        return fullname

    def __str__(self):
        return f"{self.fullname}"

    

    class Meta:
        managed = True
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"
        ordering = ["first_name", "last_name"]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

# class KnownLocation(TimeStampedModel):
#     user = OneToOneField(User, on_delete=CASCADE, related_name="knownlocations")
#     country = CharField(_("Country Name"), max_length=50, null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.fullname}"

#     class Meta:
#         managed = True
#         verbose_name = "User Known Location"
#         verbose_name_plural = "User Known Locations"
#         ordering = ["user"]

# Image upload folders

class AgentProfile(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="agentprofile")
    about = HTMLField(_("Why should they work with you?"), blank=True, null=True, max_length=500)
    company_name = CharField(_("Company Name"), blank=True, null=True, max_length=255)
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    company_address = CharField(_("Company Address"), blank=True, null=True, max_length=255)
    company_logo = ResizedImageField(size=[150, 150], quality=75, crop=['middle', 'center'], upload_to=company_logo, force_format='JPEG', null=True, help_text="image size: 150x150.")
    account_number = CharField(_("Account Number"), max_length=10, unique=True, null=True, blank=True)
    bvn = CharField(_("Bank Verification Number (BVN)"), max_length=255, null=True, blank=True, unique=True)
    bank_name = ForeignKey("Banks", on_delete=SET_NULL, related_name="userbank", null=True)
    verified = BooleanField(default=False)
    is_blocked = BooleanField(default=False)

    def __str__(self):
        return f"{self.user.fullname}"

    def title(self):
        if self.user.account_type == "Property Developers/Management Company":
            return f"{self.company_name}"
        else:
            return f"{self.user.username}"

    class Meta:
        managed = True
        verbose_name = "Agent Profile"
        verbose_name_plural = "Agent Profiles"
        ordering = ["user"]

    def get_absolute_url(self):
        """Get url for agents's detail view.

        Returns:
            str: URL for user detail.

        """
        if self.user.account_type == "Property Developers/Management Company":
            return reverse("users:company", kwargs={"slug": self.slug})
        else:
            return reverse("users:detail", kwargs={"slug": self.slug})


class UserNotification(TimeStampedModel):
    user = OneToOneField("User", on_delete=CASCADE, related_name="agentnotification")
    property_request = BooleanField(help_text=_("Recieve Notifications when someone makes request for a property?"), default=True)
    direct_message = BooleanField(help_text=_("Recieve Notifications from direct messages?"), default=True)
    email_notification = BooleanField(help_text=_("Recieve Notifications via verified email address?"), default=True)
    send_newsletter = BooleanField(_("Recieve Promotional Newsletter Emails?"), default=True)


class LoginHistory(TimeStampedModel):
    user = ForeignKey("User", on_delete=CASCADE, related_name='loginhistory')
    ip = GenericIPAddressField(
        _("User IP"), protocol="both", unpack_ipv4=False, blank=True, null=True
    )
    country = CharField(_("User Country"), blank=False, null=True, max_length=50)
    country_flag = URLField()
    latitude = FloatField(_("Location Latitude"), validators=[MinValueValidator(-90.0000000), MaxValueValidator(90.0000000)])
    longitude = FloatField(_("Location Longitude"), validators=[MinValueValidator(-180.0000000), MaxValueValidator(180.0000000)])
    city = CharField(_("Located City"), max_length=50, null=True, blank=True)
    state = CharField(_("Located State"), max_length=50, null=True, blank=True)
    language_code = CharField(_("Language Code"), max_length=3, null=True, blank=True)
    currency_symbol = CharField(_("Currency Symbol"), max_length=10, null=True, blank=True)

    def title(self):
        return f"{self.user.fullname}"

    def __str__(self):
        time = humanize.naturaltime(self.created)
        return f"{self.user.fullname} logged in at {time}"
    
class Testimonial(TimeStampedModel):
    user = OneToOneField("User", on_delete=SET_NULL, null=True, related_name="usertestimony")
    testimony = CharField(_("Testimony"), max_length=400, blank=True, null=True)
    active = BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.fullname}"

    class Meta:
        managed = True
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = [ "-created"]


class PrivacyPolicies(TimeStampedModel):
    cookies_and_tracking = BooleanField(default=True, help_text="This is a must have integration to enable us provide you with proper services and security. They do not create any security bridge for you and can only be used to login, signout and even ensure your sessions are still working. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    google_ads = BooleanField(default=True, help_text="These is an advertising and devlivey network service, aimed solely to provide advert placements based on your browser informations. permiting this allows us provide you with adverts directly on our site. Be ensured that this does not constitute any security risk to you. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    social_account_integration = BooleanField(default=True, help_text="Facebook, Instagram, Twitter, Google Plus, Linkedin, these providers are integrated into the website to ensure we have proper informations to provide for our social influence and lead generation. We do not share these information for any other purpose other than statistical analysis. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    personal_information = BooleanField(default=True, help_text="These are personal informations we collect to provide quality and personalised services to you. They include (First Name, Last Name, Phone Number, Social Accounts, Addresses, Photo). You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    commercial_information = BooleanField(default=True, help_text="These are informations we collect for commercial purposes and are used for analysis as well as providing accurate data statistics of our services usage. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    identifiers = BooleanField(default=True, help_text="These are informations we collect to prevent fraud, do analysis as well as utilize cloud services. They include Email address, device identifiers (User IDs, IP and Location). You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    internet_or_other_electronic_network_activity_information = BooleanField(default=True, help_text="These are informations we collect regarding the user interactions within the website. With this information we can provide cloud services such as Content Delivery Networks for static/asset and media files. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    age_restricktion = BooleanField(default=True, help_text="As a bid to ensure we do not share informations to individuals who are below legal age, we expect a concent to be taken, idemnifying us from any law suit involved with sharing certain or aiding a minor purchase goods and services without a concent from a legal guardian. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    ip = GenericIPAddressField(
        _("User IP"), protocol="both", unpack_ipv4=False, blank=True, null=True
    )
    country = CharField(_("Country"), max_length=80, null=True, blank=True)

    def __str__(self):
        return "new privacy policy"

    class Meta:
        managed = True
        verbose_name = "Privacy"
        verbose_name_plural = "Privacies"
        ordering = [ "-created", "-ip"]

