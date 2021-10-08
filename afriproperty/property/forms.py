from django import forms
from django.contrib.auth import get_user_model
from tinymce.widgets import TinyMCE

from .models import Property, PropertyBlueprint, PropertyImage, PropertyVideo

User = get_user_model()
    

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "property_title",
            "property_status",
            "property_type",
            "property_price_type",
            "property_price",
            "property_area",
            "property_area_number",
            "property_bedrooms",
            "property_parlors",
            "property_bathrooms",
            "property_location",
            "property_latitude",
            "property_longitude",
            "property_near_location",
            "property_city",
            "property_state",
            "property_detail",
            "property_age",
            "property_features",
            "property_expire"
        ]
        widgets = {
            "property_features": forms.CheckboxSelectMultiple(),
            "property_location": forms.TextInput(attrs={"class":"autocomplete-input", "autocomplete":"off"}),
            "property_near_location": forms.TextInput(attrs={"class":"autocomplete-input"})
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = [
            "image"
        ]

class PropertyBlueprintForm(forms.ModelForm):
    class Meta:
        model = PropertyBlueprint
        fields = [
            "image",
            "type",
            "floor_area",
            "floor_detail"
        ]

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = [
            "video"
        ]

class AgentMessageForm(forms.Form):
    property = forms.CharField()
    your_email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Email"}))
    your_phone = forms.CharField(widget=forms.NumberInput(attrs={"placeholder":"07012345678"}))
    message = forms.CharField(widget=TinyMCE(attrs={"cols":100, "row":20, "placeholder":"I am interested in this property and will like to know more about it."}))
    date_from = forms.DateField(widget=forms.DateInput())
    date_to = forms.DateField(widget=forms.DateInput())
    guests = forms.CharField(widget=forms.NumberInput())
