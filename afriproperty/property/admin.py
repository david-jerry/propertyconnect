from django.contrib import admin
from django.utils.safestring import mark_safe

from afriproperty.utils.export_as_csv import ExportCsvMixin

from .models import (
    City,
    Property,
    PropertyBlueprint,
    PropertyBookmark,
    PropertyCompare,
    PropertyImage,
    PropertyVideo,
    State,
)

# Register your models here.
admin.site.register(City)
admin.site.register(PropertyBookmark)
admin.site.register(PropertyCompare)
admin.site.register(State)
admin.site.register(PropertyImage)
admin.site.register(PropertyVideo)
admin.site.register(PropertyBlueprint)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage

class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo

class PropertyBlueprintInline(admin.TabularInline):
    model = PropertyBlueprint

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [PropertyImageInline, PropertyBlueprintInline, PropertyVideoInline]
    list_per_page = 500
    actions = ["export_as_csv"]
    list_display = ["image", "property_title", "property_price", "property_agent", "property_status", "property_type", "approved", "featured"]
    list_editable = ["property_status", "property_type", "approved", "featured"]
    list_filter = ["property_status", "property_type", "approved", "featured"]
    search_fields = ["property_title", "property_price", "property_agent", "property_status", "property_type", "approved", "featured"]
    ordering = ['-created']

    class Meta:
        model = Property

    def image(self, obj):
        print(obj)
        return mark_safe(
            f"<img src='{obj.get_image_url}' height='100' />"
        )

    def save_model(self, request, obj, form, change):
        if change:
            obj.property_agent = request.user
            obj.save()
        super().save_model(request, obj, form, change)
        

