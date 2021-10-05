import json

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from afriproperty.property.models import PropertyFeature

features = [
    {"title" : "Air Conditioning"},
    {"title" : "Swimming Pool"},
    {"title" : "Central Heating"},
    {"title" : "Laundry Room"},
    {"title" : "Gym"},
    {"title" : "Alarm"},
    {"title" : "Parking Lot"},
    {"title" : "Exercise Room"},
    {"title" : "Central Cooling"},
    {"title" : "Srorage Room"},
    {"title" : "Treated Water"},
]

class Command(BaseCommand):
    help = _("Create default features in nigeria")

    def handle(self, *args, **kwargs):

        results = features
        for i in results:
            title = i["title"]
            try:
                PropertyFeature.objects.get_or_create(property_features=title)
                print(f"{title} Feature Detail Saved")
            except:
                print(f"{title} Feature Detail Exists")

        self.stdout.write("State and City info Saved Successfully.")
