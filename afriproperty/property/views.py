import json
from decimal import Decimal

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
from django.http import JsonResponse, request
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
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
from django.views.generic.edit import FormMixin

from .filters import AddressSearchFilter, HomeSearchFilter, PropertyFilter
from .forms import (
    AgentMessageForm,
    PropertyBlueprintForm,
    PropertyForm,
    PropertyImageForm,
    PropertyVideoForm,
)
from .models import (
    Property,
    PropertyBlueprint,
    PropertyBookmark,
    PropertyCompare,
    PropertyImage,
    PropertySearchSaved,
    PropertyVideo,
)

User = get_user_model()

# Create your views here.
def property_create_view(request):
    if request.method == "POST":
        form = PropertyForm(request.POST or None)

        if form.is_valid():
            form = form.save(commit=False)
            form.property_agent = request.user
            form.save()

            image_form = PropertyImageForm(request.POST or None, request.FILES, instance=form)
            video_form = PropertyVideoForm(request.POST or None, request.FILES, instance=form)
            bp_form = PropertyBlueprintForm(request.POST or None, request.FILES, instance=form)
            if image_form.is_valid() and video_form.is_valid() and bp_form.is_valid():

                print("form ID:", form.id)
                print("form: ", form)
                
                image_form = image_form.save(commit=False)
                print("image_form: ", image_form)
                
                
                video_form = video_form.save(commit=False)
                # video_form.save()
                print("video_form: ", video_form)
                
                
                bp_form = bp_form.save(commit=False)
                # bp_form.save()
                print("bp_form: ", bp_form)

                messages.success(request, f"You have successfully updated {form.property_title}")
                return redirect(form.get_absolute_url())
            else:
                messages.success(request, f"There was an error updating {form.property_title}")
    else:
        form = PropertyForm()
        image_form = PropertyImageForm()
        video_form = PropertyVideoForm()
        bp_form = PropertyBlueprintForm()

    context = {
        "form": form,
        "image_form": image_form,
        "video_form": video_form,
        "bp_form": bp_form,
    }

    return render(request, "property/create.html", context)

def property_update_view(request, slug=None):
    obj = get_object_or_404(property, slug=slug, property_agent=request.user)
    form = PropertyForm(request.POST or None, instance=obj)
    template_name = "property/update.html"
    context = {
        "form": form,
        "obj": obj
    }
    if form.is_valid():
        form = form.save(commit=False)
        form.property_agent = request.user
        form.save()
        messages.success(request, f"You have successfully updated {form.property_title}")
        return redirect(form.get_absolute_url())
    else:
        messages.success(request, f"There was an error updating {form.property_title}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, template_name, context)


class PropertyCompareListView(ListView):
    model = PropertyCompare
    template_name = "property/compare.html"
    allow_empty = True
    context_object_name = "objects"
    ordering = ["-created"]
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)



class PropertySearchListview(ListView):
    model = Property
    template_name = 'property/filter.html'
    allow_empty = True
    context_object_name = "objects"
    ordering = ["-created"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)

    def get_queryset(self):
        request = self.request
        # queryset = super().get_queryset()
        queryset = self.queryset
        return PropertyFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context["property_total"] = self.queryset.count()
        context["filter"] = PropertyFilter(request.GET, queryset=self.queryset)
        # if intending to save search queries
        # if self.request.user.is_authenticated:
        #     url = request.get_full_path()
        #     request.session["url"] = url
        #     search = PropertySearchSaved.objects.filter(user=request.user, search_link=url, saved=True).exists()
        #     context['search'] = search
        return context


class PropertyListView(ListView):
    model = Property
    template_name = "property/list.html"
    allow_empty = True
    context_object_name = "objects"
    ordering = ["-created"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)

    def get_queryset(self):
        request = self.request
        queryset = self.queryset
        if request.user.is_authenticated:
            for obj in self.queryset:
                bookmarks = obj.bookmarkproperty.filter(user=request.user.id,)
                if bookmarks.count() > 0:
                    obj.bookmarked = True
                else:
                    obj.bookmarked = False
        return PropertyFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        context["property_total"] = self.queryset.count()
        context["filter"] = PropertyFilter(request.GET, queryset=self.queryset)
        return context

class PropertyMapListView(ListView):
    model = Property
    template_name = "property/map_list.html"
    allow_empty = True
    context_object_name = "objects"
    queryset = Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)

    def get_queryset(self):
        request = self.request
        queryset = self.queryset

        return AddressSearchFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        data_list = [
            {
                'id': obj.id,
                'get_absolute_url': str(self.request.META['HTTP_HOST'])+"/properties/"+str(obj.slug),
                "locationTitleUrl": str(self.request.META['HTTP_HOST'])+"/properties/"+str(obj.slug),
                "property_image": str(self.request.META['HTTP_HOST'])+str(obj.get_image_url),
                'sqft_total': float(obj.property_price * Decimal(obj.property_area_number)),
                'property_area': str(float(obj.property_area))+" "+"Sq/Ft",
                'property_title': obj.property_title,
                'property_location': obj.property_location,
                'property_latitude': obj.property_latitude,
                'property_longitude': obj.property_longitude,
            }
            for obj in Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)
        ]
        context["data"] = json.dumps(data_list)
        return context

class PropertyDetailView(FormMixin, SuccessMessageMixin, DetailView):
    model = Property
    template_name = "property/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "object"
    form_class = AgentMessageForm
    queryset = Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)
    success_message = "Message Sent"

    def form_valid(self, form):
        form = form.save(commit=False)
        if self.request.user.is_authenticated:
            form.property=self.get_object().property_title
            form.your_email=self.request.user.email
            form.your_phone=self.request.user.phone_number
            form.save()
        else:
            form.property=self.get_object().property_title
            form.your_email=form.cleaned_data["your_email"]
            form.your_phone=form.cleaned_data["your_phone"]
            form.save()
        return super().form_valid(form)

    def get_queryset(self):
        request = self.request
        # queryset = super().get_queryset()
        queryset = self.queryset
        return PropertyFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        # context["property_total"] = self.get_queryset.count()
        context["property_total"] = self.queryset.count()
        context["filter"] = PropertyFilter(request.GET, queryset=self.queryset)
        return context
















































































































# def mapJson(request):
#     if not request.user.is_superuser:
#         data = HttpResponseForbidden(content="You are not authorized to view this page")
#     # data_list = list(Property.objects.filter(approved=True).exclude(property_status=Property.SOLD).values())
#     data_list = [
#         {
#             'id': obj.id,
#             'get_absolute_url': obj.get_absolute_url,
#             'sqft_total': obj.sqft_total,
#             'property_area': obj.property_area,
#             'property_title': obj.property_title,
#             'property_location': obj.property_location,
#             'property_latitude': obj.property_latitude,
#             'property_longitude': obj.property_longitude,
#         }
#         for obj in Property.objects.filter(approved=True).exclude(property_status=Property.SOLD)
#     ]

#     for obj in Property.objects.filter(approved=True).exclude(property_status=Property.SOLD):
#         data_img_list = [
#             {
#                 "property_image": img.image.url,
#             }
#             for img in Property.propertyimage.first(property=obj.id)
#         ]

#     print("Data Serializers", data_list)
#     data = JsonResponse(data_list, safe=False)
#     return data
    

# @login_required
# def property_bookmarked(request, slug):
#     property = get_object_or_404(Property, slug=slug, property_agent=request.user)
