import json

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

from .models import Tip

# Create your views here.



class TipListView(ListView):
    model = Tip
    template_name = "tips/list.html"
    allow_empty = True
    context_object_name = "objects"
    ordering = ["-created"]
    page_kwarg = "page"
    paginated_by = 20
    queryset = Tip.objects.filter(approved=True).exclude(published=False)

    def get_queryset(self):
        query = self.request.GET.get('q')
        if self.queryset.exists():
            return self.queryset.filter(
                Q(title__icontains=query) | 
                Q(tip_content__icontains=query)
            ).distinct()




class TipDetailView(DetailView):
    model = Tip
    template_name = "tips/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Tip.objects.filter(approved=True).exclude(published=False)

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Tip.objects.filter(approved=True).exclude(published=False)
        if queryset.exists():
            return queryset.filter(
                Q(title__icontains=query) | 
                Q(tip_content__icontains=query)
            ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        if object.id >= 1:
            next_tip_id = object.id + 1
            previous_tip_id = object.id - 1
            next_tip = Tip.objects.filter(id=next_tip_id)
            previous_tip = Tip.object.filter(id=previous_tip_id)
            if next_tip.exists():
                print(next_tip.title)
                context["next"] = next_tip
            else:
                pass

        
            if previous_tip.exists():
                print(previous_tip.title)
                context["previous"] = previous_tip
            else:
                pass

        return context
