from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

from .models import EmailSubscribe


class EnquireForm(forms.Form):
    from_email = forms.EmailField(required=True, widget=forms.EmailInput())
    subject = forms.CharField(required=True, widget=forms.TextInput())
    message = forms.CharField(required=True, widget=TinyMCE(attrs={"cols":100, "row":20, "placeholder":"What will you like to enquire from us?"}))


class PartnershipForm(forms.Form):
    PREFERRED_CONTACT = (
        ("Mail", "Mail"),
        ("Phone", "Phone")
    )
    from_email = forms.EmailField(required=True, widget=forms.EmailInput())
    company = forms.CharField(required=True, widget=forms.TextInput())
    phone = forms.CharField(required=True, widget=forms.NumberInput())
    subject = forms.CharField(required=True, widget=forms.TextInput())
    message = forms.CharField(required=True, widget=TinyMCE(attrs={"cols":100, "row":20, "placeholder":"How can we benefit from working with you?"}))
    preferred = forms.ChoiceField(required=True, choices=PREFERRED_CONTACT, widget=forms.Select(attrs={"class":"select-input"}))

class ScamForm(forms.Form):
    from_email = forms.EmailField(required=True, widget=forms.EmailInput())
    agent_phone = forms.CharField(required=True, widget=forms.NumberInput())
    complainer_username = forms.CharField(required=True, widget=forms.TextInput())
    agent_username = forms.CharField(required=True, widget=forms.TextInput())
    agent_company = forms.CharField(required=True, widget=forms.TextInput())
    subject = forms.CharField(required=True, widget=forms.TextInput())
    message = forms.CharField(required=True, widget=TinyMCE(attrs={"cols":100, "row":20, "placeholder":"Which of our verified agents betrayed your trust? please type their number out"}))


class EmailSubscribeForm(forms.ModelForm):
    class Meta:
        model = EmailSubscribe
        fields = ["email"]

