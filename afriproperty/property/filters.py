import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Fieldset, Layout, Submit
from django import forms
from django.forms import widgets
from django.forms.widgets import HiddenInput
from django_filters.filters import RangeFilter
from django_filters.widgets import RangeWidget

from .models import City, Property, PropertyFeature, State

SOLD = "Sold"
BUY = "Buy"
RENT = "Rent"
DEVELOP = "Develop"
SHORTLET = "Shortlet"

PROPERTY_STATUS = (
    (SOLD, "Sold"),
    (BUY, "Buy"),
    (RENT, "Rent"),
    (DEVELOP, "Develop"),
    (SHORTLET, "Shortlet"),
)

APARTMENT = "Apartment"
HOUSE = "House"
COMMERCIAL = "Commercial"
GARAGE = "Garage"
GARDEN = "Garden"
LOT = "Lot"
PLOT = "Plot"

PROPERTY_TYPE = (
    (APARTMENT, "Apartment"),
    (HOUSE, "House"),
    (COMMERCIAL, "Commercial"),
    (GARAGE, "Garage"),
    (GARDEN, "Garden"),
    (LOT, "Lot"),
    (PLOT, "Plot"),
)


ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 00

ROOMS = (
    (ONE, "1  Room"),
    (TWO, "2  Rooms"),
    (THREE, "3  Rooms"),
    (FOUR, "4  Rooms"),
    (FIVE, "5  Rooms"),
    (SIX, "More than 5 Rooms"),
)

PROPERTY_AGE = (
    (1, "less than 1 Year"),
    (5, "less than 5 Years"),
    (10, "less than 10 Years"),
    (20, "less than 20 Years"),
    (50, "less than 50 Years"),
)

PROPERTY_PRICE = (
    (10000, "less than 10000"),
    (50000, "less than 50000"),
    (100000, "less than 100000"),
    (2500000, "less than 250000"),
    (5000000, "less than 500000"),
    (8500000, "less than 850000"),
)


class PropertyFilter(django_filters.FilterSet):
    property_title = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={"placeholder":"Enter address: Street, City, State"}))
    property_status = django_filters.MultipleChoiceFilter(choices=PROPERTY_STATUS, lookup_expr='icontains', widget=forms.SelectMultiple(attrs={"data-placeholder":"Any Type", "class":"chosen-select"}))
    property_type = django_filters.MultipleChoiceFilter(choices=PROPERTY_TYPE, lookup_expr='iexact', widget=forms.SelectMultiple(attrs={"data-placeholder":"Any Type", "class":"chosen-select"}))
    property_bedrooms = django_filters.ChoiceFilter(empty_label='Beds', choices=ROOMS, lookup_expr='iexact', widget=forms.Select(attrs={"data-placeholder":"Beds", "class":"chosen-select"}))
    property_bathrooms = django_filters.ChoiceFilter(empty_label='Baths', choices=ROOMS, lookup_expr='iexact', widget=forms.Select(attrs={"data-placeholder":"Baths", "class":"chosen-select"}))
    property_parlors = django_filters.ChoiceFilter(empty_label='Parlors', choices=ROOMS, lookup_expr='iexact', widget=forms.Select(attrs={"data-placeholder":"Parlors", "class":"chosen-select"}))
    property_age = django_filters.ChoiceFilter(empty_label='Age', choices=PROPERTY_AGE, lookup_expr='lte', widget=forms.Select(attrs={"data-placeholder":"Age", "class":"chosen-select"}))
    property_state = django_filters.ModelChoiceFilter(empty_label='All States', field_name="property_state", null_label='No State', queryset=State.objects.all(), widget=forms.Select(attrs={"data-placeholder":"All States", "class":"chosen-select"}))
    property_city = django_filters.ModelChoiceFilter(empty_label='All Cities', field_name="property_city", null_label='No City', queryset=City.objects.all(), widget=forms.Select(attrs={"data-placeholder":"All States", "class":"chosen-select"}))
    property_features = django_filters.ModelMultipleChoiceFilter(field_name="property_features", queryset=PropertyFeature.objects.all(), widget=forms.CheckboxSelectMultiple())
    property_area = django_filters.RangeFilter()
    property_price = django_filters.RangeFilter()

    class Meta:
        model = Property
        fields = (
            "property_title",
            "property_status",
            "property_type",
            "property_bedrooms",
            "property_bathrooms",
            "property_parlors",
            "property_area",
            "property_state",
            "property_city",
            "property_features"
        )


class HomeSearchFilter(django_filters.FilterSet):
    property_title = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={"placeholder":"Enter address: Street, City, State"}))
    property_status = django_filters.MultipleChoiceFilter(widget=forms.RadioSelect(), choices=PROPERTY_STATUS, lookup_expr='iexact')
    property_type = django_filters.MultipleChoiceFilter(choices=PROPERTY_TYPE, widget=forms.SelectMultiple(), lookup_expr='iexact')
    property_price__gte = django_filters.NumberFilter(field_name='property_price', widget=forms.NumberInput(attrs={"placeholder":"Min Price"}), lookup_expr='min__gte')
    property_price__lte = django_filters.NumberFilter(field_name='property_price', widget=forms.NumberInput(attrs={"placeholder":"Max Price"}), lookup_expr='max__lte')
    
    class Meta:
        model = Property
        fields = (
            'property_title',
            'property_status',
            'property_type',
        )


class AddressSearchFilter(django_filters.FilterSet):
    property_title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Property
        fields = [
            'property_title'
            ]
