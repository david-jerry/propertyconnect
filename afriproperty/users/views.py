import json
import os

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear, datetime
from django.db.models.query_utils import Q
from django.http import JsonResponse, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)
from django.views.generic.edit import FormMixin, ModelFormMixin

from afriproperty.property.models import Property, PropertyBookmark
from afriproperty.users.forms import (
    AgentProfileForm,
    NotificationForm,
    PrivacyPoliciesForm,
    UpdateImageForm,
    UserChangeForm,
    UserUpdateForm,
)

from .models import (
    AgentProfile,
    LoginHistory,
    PrivacyPolicies,
    Testimonial,
    UserNotification,
)

User = get_user_model()


# class UserDetailView(LoginRequiredMixin, DetailView, FormMixin):
class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = "users/user_detail.html"
    context_object_name = "object"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

user_detail_view = UserDetailView.as_view()

class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    template_name = "users/user_profile.html"
    form_class = UserUpdateForm
    context_object_name = "object"
    success_message = _("User Information successfully updated!")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user

user_profile_view = UserProfileView.as_view()


class AgentListView(ListView):
    model = AgentProfile
    template_name = 'users/agents_list.html'
    allow_empty = True
    context_object_name = "objects"
    ordering = ["user"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = AgentProfile.objects.filter(user__is_active=True, user__accept_terms=True, is_blocked=False).exclude(user__account_type="Property Developers/Management Company")

class AgentCompanyListView(ListView):
    model = AgentProfile
    template_name = 'users/company_list.html'
    allow_empty = True
    context_object_name = "objects"
    ordering = ["user"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = AgentProfile.objects.filter(user__account_type="Property Developers/Management Company", user__is_active=True, user__accept_terms=True, is_blocked=False)

class AgentDetailView(ListView):
    model = AgentProfile
    template_name = 'users/agents_dashboard.html'
    allow_empty = True
    context_object_name = "objects"
    ordering = ["user"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = AgentProfile.objects.filter(user__is_active=True, user__accept_terms=True, is_blocked=False).exclude(user__account_type="Property Developers/Management Company")

class AgentSearchView(ListView):
    model = AgentProfile
    template_name = 'users/agents_list.html'
    allow_empty = True
    context_object_name = "objects"
    ordering = ["user"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = AgentProfile.objects.filter(user__is_active=True, user__accept_terms=True, is_blocked=False)

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        return AgentProfile.objects.filter(user__is_active=True, user__accept_terms=True, is_blocked=False).filter(Q(user__username__iexact=query)|Q(user__first_name__icontains=query)|Q(company_name=query)).exclude(user__username=request.user.username, user__account_type="Individual [Searching for property]")
         
class AgentCompanyView(DetailView):

    model = AgentProfile
    template_name = 'users/agents_company.html'
    context_object_name = "object"
    ordering = ["user"]
    slug_field = "slug"
    slug_url_kwarg = "slug"

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = AgentProfile
    template_name = "users/user_form.html"
    context_object_name = "object"
    form_class = AgentProfileForm
    success_message = _("Information successfully updated and agency verified.")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user.agentprofile

    def form_valid(self, form):
        request = self.request
        user = request.user
        form_data = form.cleaned_data
        bvn = form_data["bvn"]
        acc_no = form_data["account_number"]
        bank_name = form_data["bank_name"]
        bank_code = bank_name.bank_code
        f_n = user.first_name.lower()
        l_n = user.last_name.lower()

        if not user.agentprofile.verified:
            url = "https://api.paystack.co/bvn/match"
            headers = {
                "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            datum = {
                "bvn": bvn,
                "account_number": acc_no,
                "bank_code": bank_code,
                "first_name": f_n,
                "last_name": l_n
            }
            x = requests.post(url, data=json.dumps(datum), headers=headers)
            if x.status_code != 200:
                messages.error(
                    request,
                    f"Error: {x.status_code}:  Please confirm if this is your correct bvn: {bvn}",
                )
                return reverse("users:bank")
            elif x.status_code == 200:
                results = x.json()
                print(results)

                initialized = results
                verified = initialized["status"]
                print(verified)
                blacklisted = initialized["data"]["is_blacklisted"]
                print(blacklisted)
                if not blacklisted == "true":
                    AgentProfile.objects.filter(user=user).update(verified=True)
                    messages.success(request, f"You have successfully verified your account. Enjoy extra benefits now")          
                else:
                    AgentProfile.objects.filter(user=user).update(verified=False, is_blocked=True, user__is_active=False)
                    messages.error(request, f"You account is blacklisted, and so we can not verify you at the moment. Please contact your financial institution for clarity. We shall temporarily disable this account")          
        return super().form_valid(form)

user_update_view = UserUpdateView.as_view()

class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

user_redirect_view = UserRedirectView.as_view()

class NotificationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserNotification
    template_name = "users/user_notification.html"
    form_class = NotificationForm
    context_object_name = "object"
    success_message = _("You have successfully updated your notifications settings.")

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

    # def get_initial(self):
    #     initial = super().get_initial()
    #     img = self.request.user.image.path
    #     if self.request.user:
    #         initial["image"] = img
    #     return initial

    def get_object(self):
        return self.request.user.agentnotification

    def form_valid(self, form):
        form = form.save(commit=False)
        if self.request.user.agentnotification:
            form.user = self.request.user
            form.save()
            return self.get_success_url()

user_notification_view = NotificationView.as_view()








class UserBookmarks(LoginRequiredMixin, ListView):
    model = PropertyBookmark
    template_name = "users/bookmarked_property.html"
    allow_empty = True
    ordering = ["-created"]
    page_kwarg = "page"
    paginated_by = 20
    context_object_name = "objects"

    def get_queryset(self):
        return PropertyBookmark.objects.filter(user=self.request.user)


class AgentProperties(LoginRequiredMixin, ListView):
    model = Property
    template_name = "users/user_manage_property.html"
    allow_empty = True
    ordering = ["-created"]
    page_kwarg = "page"
    paginated_by = 20
    context_object_name = "objects"

    def get_queryset(self):
        if self.request.user.account_type != "Individual [Searching for property]":
            return Property.objects.filter(property_agent=self.request.user)










class PrivacyPoliciesView(SuccessMessageMixin, CreateView):
    model = PrivacyPolicies
    form_class = PrivacyPoliciesForm
    template_name = "users/privacy_form.html"

    def form_valid(self, form):
        form = form.save(commit=False)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            response = requests.get(f"https://reallyfreegeoip.org/jscon/{ip}")
            request.session["geodata"] = response.json()
            geodata = request.session["geodata"]
            country = geodata["country_name"]
            form.country = country
            form.ip = ip
            form.save()
            messages.success(request, "Thank you for accepting our policies.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
        except:
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

class PrivacyUpdateView(SuccessMessageMixin, UpdateView):
    model = PrivacyPolicies
    form_class = PrivacyPoliciesForm
    template_name = "users/privacy_update_form.html"

    def form_valid(self, form):
        form = form.save(commit=False)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            response = requests.get(f"https://reallyfreegeoip.org/jscon/{ip}")
            request.session["geodata"] = response.json()
            geodata = request.session["geodata"]
            country = geodata["country_name"]
            form.country = country
            form.ip = ip
            form.save()
            messages.success(request, "You successfully updated your policy permissions. if some part of our site seem inaccessible this will be due to the restrictions you limited for use to serve you better. Please do not contact us directly.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))
        except:
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))


def accept_all_policies(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        response = requests.get(f"https://reallyfreegeoip.org/jscon/{ip}")
        request.session["geodata"] = response.json()
        geodata = request.session["geodata"]
        country = geodata["country_name"]
        PrivacyPolicies.objects.filter(ip=ip, country=country).update(
            social_account_integration  = True,
            personal_information = True,                 
            commercial_information = True,
            identifiers = True,
            internet_or_other_electronic_network_activity_information = True,
            age_restricktion = True,
            country = country,
            modified=datetime.datetime.now()
        )
    except PrivacyPolicies.DoesNotExist:             #-----Here My Edit
        response = requests.get(f"https://reallyfreegeoip.org/jscon/{ip}")
        request.session["geodata"] = response.json()
        geodata = request.session["geodata"]
        country = geodata["country_name"]
        PrivacyPolicies.objects.create(
            ip=ip, 
            social_account_integration  = True,
            personal_information = True,                 
            commercial_information = True,
            identifiers = True,
            internet_or_other_electronic_network_activity_information = True,
            age_restricktion = True,
            country = country,
            modified=datetime.datetime.now()
        )
    return None

def reject_all_policies(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        response = requests.get(f"https://reallyfreegeoip.org/jscon/{ip}")
        request.session["geodata"] = response.json()
        geodata = request.session["geodata"]
        country = geodata["country_name"]
        PrivacyPolicies.objects.filter(ip=ip, country=country).update(
            social_account_integration  = False,
            personal_information = False,                 
            commercial_information = False,
            identifiers = False,
            internet_or_other_electronic_network_activity_information = False,
            age_restricktion = False,
            country = country,
            modified=datetime.datetime.now()
        )
    except PrivacyPolicies.DoesNotExist:             #-----Here My Edit
        response = requests.get(f"https://reallyfreegeoip.org/jscon/{ip}")
        request.session["geodata"] = response.json()
        geodata = request.session["geodata"]
        country = geodata["country_name"]
        PrivacyPolicies.objects.create(
            ip=ip, 
            social_account_integration  = False,
            personal_information = False,                 
            commercial_information = False,
            identifiers = False,
            internet_or_other_electronic_network_activity_information = False,
            age_restricktion = False,
            country = country,
            modified=datetime.datetime.now()
        )
    return None


