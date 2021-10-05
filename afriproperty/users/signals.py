import datetime
import json

import requests
from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import AgentProfile, LoginHistory, Testimonial, UserNotification

User = get_user_model()

today = datetime.date.today()


# Log and save user signup location and IP on every login attempt

@receiver(user_logged_in)
def login_user_ip(request, sender, user, **kwargs):
    print("Login signal working fine")
    if user:
        url = "https://find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com/iplocation"
        headers = {
            'x-rapidapi-host': "find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com",
            'x-rapidapi-key': "d2ee03b153msh7f9f91df901fa08p163f4ajsn694bb6dda556"
        }
        response = requests.request("GET", url, headers=headers, params={'apikey': settings.IPLOCATION_APIKEY})
        if response.status_code != 200:
            return str(response.status_code)

        results = response.json()
        print("results: ", results)
        if results["status"] == 200:
            ip = results["ip"]
            city = results["city"]
            country = results["country"]
            country_flag = results["flag"]
            latitude = results["latitude"]
            longitude = results["longitude"]
            state = results["state"]
            language_code = results["languages"][:2]
            currency_symbol = results["currencySymbolNative"]
            LoginHistory.objects.create(user=user, language_code=language_code, currency_symbol=currency_symbol, country_flag=country_flag, latitude=latitude, longitude=longitude, ip=ip, state=state, city=city, country=country)
            
            # Send an email if location is not one of the known location on signin
            email = {
                "title": "Unusual Signin Location !",
                "shortDescription": "There was an unusual signin from an unknown location.",
                "message": "There was a signin request for your account from a unknonw location. Please verify this was you or lodge a complaint to our support@afriproperty.ng email address. We aim to keep your account safe and express our gratitude to your continued patronage."
            }
            subject = "[AfriProperty NG] Unknown Signin Request"
            to_email = user.email
            # send_mail(
                # subject=subject,
                # text_email=text_email,
                # message=message,
                # from_email=from_email,
                # to_email=to_email,
                # html_message=html_message,
                # fail_silently=False
            # )
        else:
            pass




# One to one field relational settings tied to user

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, *args, **kwargs):
    if created:
        AgentProfile.objects.get_or_create(user=instance)
        UserNotification.objects.get_or_create(user=instance)
        Testimonial.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profiles(sender, instance, created, *args, **kwargs):
    if created:
        instance.agentprofile.save()
        instance.agentnotification.save()
        instance.usertestimony.save()

from afriproperty.utils.unique_slug_generator import unique_slug_generator


# Signals Agent Profile
@receiver(post_save, sender=AgentProfile)
def create_property_slug(sender, instance, *args, **kwargs):
	if not instance.is_blocked and instance.user and not instance.slug:
		instance.slug = unique_slug_generator(instance)


@receiver(post_save, sender=AgentProfile)
def block_user(sender, created, instance, *args, **kwargs):
    if instance.is_blocked:
        User.objects.filter(username=instance.user.username).update(is_active=False)




# Testimonial Signal

@receiver(post_save, sender=Testimonial)
def user_testified(sender, created, instance, *args, **kwargs):
    if instance.active:
        User.objects.filter(username=instance.user.username).update(has_testified=True)

