import json
import re

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Property, PropertyBookmark, PropertyCompare

User = get_user_model()

@login_required()
def mark_property_purchased(request):
    """
    Api to mark a property as purchased by the buyer without page reload using vue or htmx
    """
    data = json.loads(request.body)
    property = data['property_id']
    if not property.property_status == Property.SOLD and property.property_sold:
        property.update(property_status = Property.SOLD)
        messages.success(request, f"You have successfully completed {property.property_title} purchase.")
    return JsonResponse({"success": True})

@login_required
def mark_property_sold(request):
    """
    Api to mark a property as sold without page reload using vue or htmx
    """
    data = json.loads(request.body)
    property = data['property_id']
    if not property.property_status == Property.SOLD:
        property.update(property_sold = True)
        messages.info(request, f"{property.property_agent.fullname}, You have successfully completed {property.property_title} sale.")
    return JsonResponse({"success": True})

@login_required
def property_delete(request):
    """
    Api to add delete a property that is not sold or rented yet without page reload using vue or htmx
    """
    data = json.loads(request.body)
    property = data['property_id']
    if not property.property_status == Property.SOLD and property.property_sold:
        property.delete()
        messages.info(request, f"{property.property_agent.fullname}, You have successfully removed {property.property_title} from property listing.")
    return JsonResponse({"success": True})






def add_property_compare(request):
    data = json.loads(request.body)
    property = data['property_id']

    if not PropertyCompare.objects.filter(property_id=property).exists():
        compare = PropertyCompare.objects.create(property_id=property)
        property = Property.objects.get(pk=property)
    return JsonResponse({"success": True})

def remove_property_compare(request):
    data = json.loads(request.body)
    property = data['property_id']

    if PropertyCompare.objects.filter(property_id=property).exists():
        compare = PropertyCompare.objects.filter(property_id=property).delete()
        property = Property.objects.get(pk=property)
    return JsonResponse({"success": True})






@login_required
def add_bookmark_api(request):
    """
    Api to add bookmarks directly to their respective view without page reload using vue or htmx
    """
    data = json.loads(request.body)
    property_id = data['property_id']

    if not PropertyBookmark.objects.filter(property_id=property_id).filter(user=request.user, active=True).exists():
        bookmark = PropertyBookmark.objects.create(property_id=property_id, user=request.user, active=True)
        property = Property.objects.get(pk=property_id)
        # messages.info(request, f"You just bookmarked this item {property.property_title}")
    else:
        bookmark = PropertyBookmark.objects.filter(property_id=property_id, user=request.user).delete()
        property = Property.objects.get(pk=property_id)
        # messages.info(request, f"You just unbookmarked this item {property.property_title}")
    return JsonResponse({"success": True})


@login_required
def remove_bookmark_api(request):
    """
    Api to remove bookmarks directly to their respective view without page reload using vue or htmx
    """
    data = json.loads(request.body)
    property_id = data['property_id']

    if PropertyBookmark.objects.filter(property_id=property_id).filter(user=request.user, active=True).exists():
        bookmark = PropertyBookmark.objects.filter(property_id=property_id, user=request.user, active=True).delete()
        property = Property.objects.get(pk=property_id)
        # messages.info(request, f"You just bookmarked this item {property.property_title}")
    return JsonResponse({"success": True})
