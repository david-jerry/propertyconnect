import os

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import BadHeaderError, EmailMessage, send_mail, send_mass_mail
from django.http import Http404, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from afriproperty.property.filters import (
    AddressSearchFilter,
    HomeSearchFilter,
    PropertyFilter,
)
from afriproperty.property.models import Property

from .forms import EmailSubscribeForm, EnquireForm, PartnershipForm, ScamForm
from .models import EmailSubscribe


# Create your views here.
def home_view(request):
    f = HomeSearchFilter(request.GET, queryset=Property.objects.filter(approved=True).exclude(property_status=Property.SOLD))
    context = {"filter":f,}
    return render(request, 'pages/home.html', context)

def contact_view(request):
    if request.method == 'GET':
        form = EnquireForm()
    else:
        form = EnquireForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            result_message = f"{subject}\n\n{message}"
            html_message = render_to_string('email/support_mail.html', {'message': message, 'from_email': from_email, 'subject': subject})

            try:
                send_mail(subject, result_message, from_email, ['office@propertyconnect.ng'], html_message=html_message, fail_silently=False)
                messages.success(request, "Your enquiry has been sent successfully")
            except BadHeaderError:
                messages.error(request, "There was an error sending yout email at the moment, please try again later.")
                return HttpResponse('Invalid Header found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'pages/contact.html', {'form': form})

def partnership_apply_view(request):
    if request.method == 'GET':
        form = PartnershipForm()
    else:
        form = PartnershipForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            company = form.cleaned_data['company']
            phone = form.cleaned_data['phone']
            preferred = form.cleaned_data['preferred']
            message = form.cleaned_data['message']
            result_message = f"{subject}\n\n{company} - {phone} has requested to have a partnership with you.\n\n\nMessage: {message}\n\nPreferred Mode of communication: {preferred} "
            html_message = render_to_string('email/support_mail.html', {'message': message, 'from_email': from_email, 'company': company, 'phone': phone, 'subject': subject, "preferred": preferred})

            try:
                send_mail(subject, result_message, from_email, ['partners@propertyconnect.ng'], html_message=html_message, fail_silently=False)
                messages.success(request, "Your application for a partnership has been sent successfully, we shall reply to you email address shortly or give you a call if necessary. Thank you.")
            except BadHeaderError:
                messages.error(request, "There was an error sending yout email at the moment, please try again later.")
                return HttpResponse('Invalid Header found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'pages/partnership.html', {'form': form})

def scam_report_view(request):
    if request.method == 'GET':
        form = ScamForm()
    else:
        form = ScamForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            complainer_username = form.cleaned_data['complainer_username']
            agent_phone = form.cleaned_data['agent_phone']
            agent_username = form.cleaned_data['agent_username']
            agent_company = form.cleaned_data['agent_company']
            message = form.cleaned_data['message']
            result_message = f"{subject}\n\n{complainer_username}\n\n{message}\n\nAgent Details:\nComapny:{agent_company}\nPhone:{agent_phone}\nUsername:{agent_username}"
            html_message = render_to_string('email/scam.html', {'agent_company':agent_company, 'message': message, 'from_email': from_email, 'agent_phone':agent_phone, 'agent_username': agent_username, 'subject': subject})

            try:
                send_mail(subject, result_message, from_email, ['report@propertyconnect.ng'], html_message=html_message, fail_silently=False)
                messages.success(request, "Your report has been received and adequate action has already started to ensure we keep our site free from miscriants. Thank you for your support.")
            except BadHeaderError:
                messages.error(request, "There was an error sending yout email at the moment, please try again later.")
                return HttpResponse('Invalid Header found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'pages/scam.html', {'form': form})

def subscribe_view(request):
    if request.method == 'GET':
        form = EmailSubscribeForm()
    else:
        form = EmailSubscribeForm(request.POST)
        if form.is_valid():
            subject = "[Property Connect] Email Subscription Activated"
            from_email = "noreply@propertyconnect.ng"
            sub_email = form.cleaned_data['email']
            message = f"You have successfully activated the option to receive promotional emails with this email address {sub_email} from us. \n Please find bellow our link to unsubscribe if this was opt-in by an error."
            html_message = render_to_string('email/email_subscribe.html', {'message': message, 'from_email': from_email, 'sub_email':sub_email, 'subject': subject})
            form.active = True
            form.save()
            try:
                send_mail(subject, message, from_email, [sub_email], html_message=html_message, fail_silently=False)
                messages.success(request, "You have successfully subscribed for promotional emails")
            except BadHeaderError:
                messages.error(request, "Your subscription failed.")
                return HttpResponse('Invalid Header found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'pages/subscribe.html', {'form': form})


def unsubscribe_view(request, id):
    subscriber = get_object_or_404(EmailSubscribe, id=id)
    if subscriber.exists():
        subscriber.update(active=False)
        messages.success(request, "You have successfully unsubscribe to our mailing list")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
