from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from afriproperty.users.forms import UserChangeForm, UserCreationForm
from afriproperty.utils.export_as_csv import ExportCsvMixin

from .models import AgentProfile, Banks, LoginHistory, Testimonial, UserNotification

User = get_user_model()

admin.site.register(Banks)
admin.site.register(LoginHistory)
admin.site.register(Testimonial)
admin.site.register(UserNotification)


@admin.register(AgentProfile)
class AgentProfile(admin.ModelAdmin, ExportCsvMixin):
    model = AgentProfile
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = [
        "__str__",
        'company_name',
        "company_address",
        "bvn",
        'verified',
        'is_blocked'
    ]
    list_editable = [
        'is_blocked',
    ]
    actions = [
        "export_as_csv",
    ]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ExportCsvMixin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (_("Authentication Info"), {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("account_type", "first_name", "last_name", "phone_number", "postcode")}),
        (_("Social info"), {"fields": ("facebook", "linkedin", "instagram")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "accept_terms",
                    "has_testified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "account_type", "first_name", "last_name", "phone_number", "accept_terms", "has_testified", "is_active", "is_superuser"]
    list_editable = ["account_type", "has_testified", "is_active"]
    search_fields = ["first_name", "last_name", "phone_number"]
    actions = [
        "export_as_csv",
    ]
