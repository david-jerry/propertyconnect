import json

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from afriproperty.users.models import AgentProfile, Banks

# from requests_html import HTMLSession


User = get_user_model()


class Command(BaseCommand):
    help = _("Collect all bank registered from paystack")

    def handle(self, *args, **kwargs):
        url = "https://api.paystack.co/bank"
        headers = {
            "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        datum = {"country": "nigeria", "use_cursor": True, "perPage": 100}
        x = requests.get(url, data=json.dumps(datum), headers=headers)
        if x.status_code != 200:
            return str(x.status_code)

        results = x.json()
        for i in results["data"]:
            bank_id = i["id"]
            bank_name = i["name"]
            bank_slug = i["slug"]
            bank_code = i["code"]
            # bank_lcode = i["longcode"]
            bank_country = i["country"]
            bank_currency = i["currency"]
            # Banks.objects.create(country=bank_country, bank_id=bank_id, title=bank_name, slug=bank_slug, bank_code=bank_code, currency=bank_currency)
            try:
                Banks.objects.create(country=bank_country, bank_id=bank_id, title=bank_name, slug=bank_slug, bank_code=bank_code, currency=bank_currency)
            except:
                print(f"{bank_name} Bank Detail Exists")
        self.stdout.write("Banks Saved Successfully.")
