from django.contrib import admin
from django.utils.safestring import mark_safe

from afriproperty.utils.export_as_csv import ExportCsvMixin

from .models import Tip, TipImageFile, TipVideoFile

# Register your models here.
admin.site.register(TipImageFile)
admin.site.register(TipVideoFile)


class PropertyImageInline(admin.TabularInline):
    model = TipImageFile

class PropertyVideoInline(admin.TabularInline):
    model = TipVideoFile


@admin.register(Tip)
class PropertyAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [PropertyImageInline, PropertyVideoInline]
    list_per_page = 500
    actions = ["export_as_csv"]
    list_display = ["image", "title", "tip_type", "published", "approved", "featured"]
    list_editable = ["title", "tip_type", "published", "approved", "featured"]
    list_filter = ["title", "tip_type", "published", "approved", "featured"]
    search_fields = ["title", "tip_type", "published", "approved", "featured"]
    ordering = ['-created']

    class Meta:
        model = Tip


    def image(self, obj):
        print(obj)
        return mark_safe(
            "<img src='" + str(obj.get_image_url) + "' height='100' />"
        )

    def save_model(self, request, obj, form, change):
        if change:
            obj.tip_author = request.user
            obj.save()
        super().save_model(request, obj, form, change)
