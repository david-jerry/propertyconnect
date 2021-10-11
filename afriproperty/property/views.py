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
from django.forms.models import inlineformset_factory, modelformset_factory
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
    PropertyBlueprintFormset,
    PropertyForm,
    PropertyImageForm,
    PropertyImageFormset,
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
class PropertyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PropertyForm
    template_name = "property/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video_form'] = PropertyVideoForm()
        context['image_formset'] = PropertyImageFormset()
        context['bp_formset'] = PropertyBlueprintFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_formset = PropertyImageFormset(request.POST or None, request.FILES)
        bp_formset = PropertyBlueprintFormset(request.POST or None, request.FILES)
        video_form = PropertyVideoForm(request.POST or None, request.FILES)
        if form.is_valid() and image_formset.is_valid() and bp_formset.is_valid() and video_form.is_valid():
            return self.form_valid(form, image_formset, bp_formset, video_form)
        else:
            return self.form_invalid(form, image_formset, bp_formset, video_form)

    def form_valid(self, form, image_formset, bp_formset, video_form):
        self.object = form.save(commit=False)
        self.object.save()

        image_form = image_formset.save(commit=False)
        for form in image_form:
            form.property = self.object
            form.save()

        bp_form = bp_formset.save(commit=False)
        for form in bp_form:
            form.property = self.object
            form.save()


        vid_form = video_form.save(commit=False)
        vid_form.property = self.object
        vid_form.save()

        return redirect(reverse("property:list"))

    def form_invalid(self, form, image_formset, bp_formset, video_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                image_formset=image_formset,
                bp_formset=bp_formset,
                video_form=video_form
            )
        )

property_create_view = PropertyCreateView.as_view()

# def property_create_view(request):
#     qs = PropertyImage.objects.all()
#     bp = PropertyBlueprint.objects.all()
#     pr = Property()

#     form = PropertyForm(request.POST or None, instance=pr)

#     image_form_formset = inlineformset_factory(PropertyImage, extra=0, form=PropertyImageForm)
#     image_formset = image_form_formset()

#     video_form = PropertyVideoForm(request.POST or None, request.FILES)

#     bp_form_formset = modelformset_factory(PropertyBlueprint, extra=0, form=PropertyBlueprintForm)
#     bp_formset = bp_form_formset()

#     context = {
#         "form": form,
#         "image_formset": image_formset,
#         "video_form": video_form,
#         "bp_formset": bp_formset,
#     }

#     if request.POST:
#         image_formset = image_form_formset(request.POST or None, request.FILES, queryset=None)
#         bp_formset = bp_form_formset(request.POST or None, request.FILES, queryset=None)
#         if form.is_valid() and image_formset.is_valid() and video_form.is_valid() and bp_formset.is_valid():
#             form = form.save(commit=False)
#             form.property_agent = request.user
#             form.approved = True
#             form.save()

            
#             for image_form in image_formset:
#                 image_form = image_form.save(commit=False)
#                 if image_form.property is None:
#                     image_form.property = form
#                 image_form.save()
            
            
#             for bp_form in bp_formset:
#                 bp_form = bp_form.save(commit=False)
#                 if bp_form.property is None:
#                     bp_form.property = form
#                 bp_form.save()
            
            
#             video_form = video_form.save(commit=False)
#             video_form.property = form
#             video_form.save()     

#             messages.success(request, f"You have successfully created a property listing")
#             return redirect(reverse_lazy("property:list"))
#         else:
#             messages.success(request, f"There was an error creating a property listing")


#     return render(request, "property/create.html", context)

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
