from django.conf import settings

from afriproperty.property.models import City, Property, PropertyCompare
from afriproperty.tips.models import Tip


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {
        "DEBUG": settings.DEBUG,
        "API_KEY": settings.GOOGLE_API_KEY,
        "featured_tips": Tip.objects.filter(approved=True, featured=True).exclude(published=False).order_by("-created")[:3],
        "lagos": City.objects.get(title__icontains="Lagos"),
        "abuja": City.objects.get(title__icontains="Abuja"),
        "rivers": City.objects.get(title__icontains="Port Harcourt"),
        "ibadan": City.objects.get(title__icontains="Ibadan"),
        "featured_properties": Property.objects.filter(featured=True),
        "recent_properties": Property.objects.filter(approved=True).order_by('-created')[:10],
        "all_properties": Property.objects.filter(approved=True).exclude(property_status=Property.SOLD).order_by("-created"),
        "compared_properties": PropertyCompare.objects.all().order_by("-created")[:3],
    }
