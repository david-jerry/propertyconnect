from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from afriproperty.users.models import (
    AgentProfile,
    PrivacyPolicies,
    Testimonial,
    UserNotification,
)

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "image",
            "phone_number",
            "postcode",
            "facebook",
            "linkedin",
            "instagram",
        ]

class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "postcode",
            "account_type",
            "accept_terms",
        ]


class NotificationForm(forms.ModelForm):
    class Meta:
        model = UserNotification
        fields = [
            "property_request",
            "direct_message",
            "email_notification",
            "send_newsletter"
        ]


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image"]


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "postcode",
            "account_type",
            "accept_terms",
        ]



        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = [
            "about",
            "company_name",
            "company_address",
            "company_logo",
            "account_number",
            "bvn",
            "bank_name"
        ]
        widgets = {
            "bank_name": forms.Select(attrs={"data-placeholder":"All Nigerian Banks", "class":"chosen-select"})
        }

class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["testimony"]


class PrivacyPoliciesForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicies
        fields = [
            "cookies_and_tracking",
            "google_ads",
            "social_account_integration",
            "personal_information",
            "commercial_information",
            "age_restricktion"
        ]
