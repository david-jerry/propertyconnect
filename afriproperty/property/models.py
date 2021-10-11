from __future__ import absolute_import

# development system imports
import os
import random
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags import humanize
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    ManyToManyField,
    OneToOneField,
    PositiveIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.db.models.fields import FloatField
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

User = settings.AUTH_USER_MODEL

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
char_regex = RegexValidator(regex=r'^[A-Za-z]*$', message="Field must be only alphabets: A-Z or a-z")

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def property_images(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "property-photo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

def blueprint_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "property-blueprint/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

def property_video(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "property-video/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

# Create your models here.
class City(TimeStampedModel):
    title = CharField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        managed = True
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["title"]

class State(TimeStampedModel):
    title = CharField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        managed = True
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["title"]


class PropertyFeature(TimeStampedModel):
    AC = "Air Conditioning"
    POOL = "Swimming Pool"
    HEAT = "Central Heating"
    LAUNDRY = "Laundry Room"
    GYM = "Gym"
    ALARM = "Alarm"
    INTERNET = "Internet"
    GARAGE = "Garage"
    GARDEN = "Garden"
    PARKING = "Parking Lot"
    EXERCISE = "Exercise Room"
    COOLING = "Central Cooling"
    STORAGE = "Srorage Room"
    WATER = "Treated Water"

    PROPERTY_FEATURES = (
        (AC, "Air Conditioning"),
        (POOL, "Swimming Pool"),
        (HEAT, "Central Heating"),
        (LAUNDRY, "Laundry Room"),
        (PARKING, "Parking Lot"),
        (EXERCISE, "Exercise Room"),
        (COOLING, "Central Cooling"),
        (STORAGE, "Srorage Room"),
        (WATER, "Treated Water"),
        (INTERNET, "Internet"),
        (GARAGE, "Attached Garage"),
        (GARDEN, "Garden"),
        (GYM, "Gym"),
        (ALARM, "Alarm"),
    )

    property_features = CharField(_("Property Features (Optional)"), max_length=17, choices=PROPERTY_FEATURES, default=POOL, null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.property_features)

    class Meta:
        managed = True
        verbose_name = "Property Feature"
        verbose_name_plural = "Property Features"
        ordering = ["property_features"]


class Property(TimeStampedModel):
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

    ANNUAL = "Annually"
    MONTHLY = "Monthly"
    SQFT = "Sq/Ft"

    PRICE_TYPE = (
        (ANNUAL , "Annually"),
        (MONTHLY , "Monthly"),
        (SQFT , "Sq/Ft"),
    )


    ZEROONE = "0 - 1"
    ZEROFIVE = "0 - 5"
    ZEROTEN = "0 - 10"
    ZEROTWENTY = "0 - 20"
    ZEROFIFTY = "0 - 50"
    FITYPLUS = "50 - more"

    PROPERTY_AGE = (
        (ZEROONE, "0 - 1"),
        (ZEROFIVE, "0 - 5"),
        (ZEROTEN, "0 - 10"),
        (ZEROTWENTY, "0 - 20"),
        (ZEROFIFTY, "0 - 50"),
        (FITYPLUS, "50 - more"),
    )

    property_agent = ForeignKey(User, on_delete=CASCADE, related_name="agentproperty")
    property_title = CharField(_("Property Title"), null=True, blank=False, max_length=500)
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    property_status = CharField(_("Property Status"), max_length=8, choices=PROPERTY_STATUS, default=RENT, null=True, blank=True)
    property_type = CharField(_("Property Type"), max_length=15, choices=PROPERTY_TYPE, default=APARTMENT, null=True, blank=True)
    
    property_price_type = CharField(_("Property Price Type"), max_length=15, choices=PRICE_TYPE, default=ANNUAL, null=True, blank=False)
    property_price = DecimalField(_("Property Price (for 1 year or 1 sq/ft)"), max_digits=20, decimal_places=2, default=0.00, blank=False, help_text="if your price type is sq/ft, then the price cost should be by a unit of the property area square feet and leave the total we will automatically round it up for you by the total area numbers you have ")
    property_area = DecimalField(_("Per Sq/Ft"), max_digits=20, decimal_places=2, default=0.00, blank=True)
    property_area_number = IntegerField(_("How many sq/ft do you have of the above property per sq/ft? i.e (5 Per Sq/Ft x 10 = 50 Total Square Feet) leave it empty for rented properties"), default=1, null=True, blank=True, help_text="From 1-1000. to calculate to total price for square feets")
    
    property_bathrooms = IntegerField(_("Bath Rooms"), choices=ROOMS, default=ONE, null=True, blank=False)
    property_bedrooms = IntegerField(_("Bed Rooms"), choices=ROOMS, default=ONE, null=True, blank=False)
    property_parlors = IntegerField(_("Parlors"), choices=ROOMS, default=ONE, null=True, blank=False)

    property_latitude = FloatField(_("Map Latitude"), null=True, default=0.000000000, validators=[MinValueValidator(-90.000000000), MaxValueValidator(90.000000000)], help_text="You can find this on google maps by inputing the actual property address and right clicking on the location pointer to reveal the latitude")
    property_longitude = FloatField(_("Map Longitude"), null=True, default=0.000000000, validators=[MinValueValidator(-180.000000000), MaxValueValidator(180.000000000)], help_text="You can find this on google maps by inputing the actual property address and right clicking on the location pointer to reveal the longitude")
    property_location = CharField(_("Property Street Address"), max_length=500, null=True, blank=False, help_text="eg. 123 Close, Street  !!! PS: Do not attach a state or country when listing this property !!!")
    property_near_location = CharField(_("Property Closest building street address"), max_length=500, null=True, blank=False, help_text="eg. 123 Close, Street  !!! PS: Do not attach a state or country when listing this property !!!")
    property_city = ForeignKey("City", on_delete=SET_NULL, null=True, related_name="propertycity")
    property_state = ForeignKey("State", on_delete=SET_NULL, null=True, related_name="propertystate")
    
    property_detail = HTMLField()
    property_age = CharField(_("Building Age (Optional)"), max_length=50, null=True, choices=PROPERTY_AGE, default=ZEROFIVE, blank=True)
    property_features = ManyToManyField("PropertyFeature", help_text="Select all features that apply for the house")
    property_expire = IntegerField(_("How long is the renting or buying supposed to last, 1 year or more?"), default=0*455, null=True, blank=True, help_text="use 100 if it a land that is being purchased. and any figure when it is a rentage. NOTE: An additional 2 months is given to a property before it is reactivated as availble for purchase after its last purchased date")

    property_sold = BooleanField(default=False)

    approved = BooleanField(default=False)
    featured = BooleanField(default=False)

    def total_area(self):
        if self.property_area and self.property_area_number:
            return self.property_area * Decimal(self.property_area_number)

    def sqft_total(self):
        if self.property_price and self.property_area_number:
            return self.property_price * Decimal(self.property_area_number)

    def last_purchased_date(self):
        if self.property_sold:
            return datetime.date.today()

    def next_expiry_date(self):
        if self.last_purchased_date and self.property_expire > 0 and self.property_expire < 100:
            return self.last_purchased_date + timedelta(days=self.property_expire) 
    
    def now_availble(self):
        today = datetime.date.today() 
        if today > self.next_expiry_date and self.property_sold:
            self.property_sold = False
            self.property_sold.save()
            return True
        return False


    def formated_address(self):
        return self.property_location.replace(" ", "+")

    def formated_state(self):
        return self.property_state.title.replace(" ", "+")

    def formated_closest_address(self):
        return self.property_near_location.replace(" ", "+")

    def __str__(self):
        return str(self.property_title)

    def title(self):
        return self.property_title


    def get_related_property(self):
        return Property.objects.filter(property_agent=self.property_agent, property_type=self.property_type, property_state=self.property_state, approved=True).exclude(property_title=self.property_title)[:4]

    def get_featured_property(self):
        return Property.objects.filter(property_agent=self.property_agent, property_type=self.property_type, property_state=self.property_state, approved=True, featured=True).exclude(property_title=self.property_title)[:4]

    def get_related_property_by_agent(self):
        return Property.objects.filter(property_agent=self.property_agent)[:10]

    def get_related_property_by_state(self):
        return Property.objects.filter(property_state=self.property_state)[:10]

    @property
    def get_image_url(self):
        img = self.propertyimage.first()
        if img:
            return img.image.url
        return None

    def get_all_images(self):
        return self.propertyimage.all()

    def get_all_floors(self):
        return self.propertyplan.all()

    def get_video_url(self):
        img = self.propertyvideo.first()
        if img:
            return img.video.url
        return None


    class Meta:
        managed = True
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-created", "property_title"]

    def get_absolute_url(self):
        """Get url for blog's detail view.

        Returns:
            str: URL for blog detail.

        """
        return reverse("property:detail", kwargs={"slug": self.slug})


    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"


class PropertyImage(TimeStampedModel):
    property = ForeignKey("Property", on_delete=CASCADE, related_name="propertyimage")
    image = ResizedImageField(size=[520, 397], quality=80, crop=['middle', 'center'], upload_to=property_images, force_format='JPEG', null=True, blank=True, help_text="image size: 520x397.")

    def __str__(self):
        return f"{self.property.property_title} Image"

class PropertyBlueprint(TimeStampedModel):
    GROUND = "Ground Floor"
    FIRST = "First Floor"
    SECOND = "Second Floor"
    THIRD = "Third Floor"
    FOURTH = "Fourth Floor"
    ALL = "All Floor Type"
    PENTHOUSE = "Penthouse"
    GARAGE = "Garage"
    POOL_HOUSE = "Pool House"

    BLUEPRINT = (
        (GROUND, "Ground Floor"),
        (FIRST, "First Floor"),
        (SECOND, "Second Floor"),
        (THIRD, "Third Floor"),
        (FOURTH, "Fourth Floor"),
        (ALL, "All Floor Type"),
        (PENTHOUSE, "Penthouse"),
        (GARAGE, "Garage"),
        (POOL_HOUSE, "Pool House"),
    )
    property = ForeignKey("Property", on_delete=CASCADE, related_name="propertyplan")
    type = CharField(_("Blueprint"), null=True, blank=False, max_length=50, choices=BLUEPRINT, default=FIRST)
    image = ResizedImageField(size=[1000, 576], quality=70, crop=['middle', 'center'], upload_to=blueprint_image, force_format='JPEG',  null=True, blank=True, help_text="image size: 1000x576.")
    floor_area = DecimalField(_("Area Sq/Ft"), max_digits=20, decimal_places=2, default=0.00, blank=False)
    floor_detail = HTMLField()

    def __str__(self):
        return f"{self.property.property_title} {self.type} Blueprint"

class PropertyVideo(TimeStampedModel):
    property = ForeignKey("Property", on_delete=CASCADE, related_name="propertyvideo")
    video = FileField(upload_to=property_video, null=True, blank=True, help_text="Your video should be 40Seconds Long, 20MB in size max")

    def __str__(self):
        return f"{self.property.property_title} New Video"






class PropertyCompare(TimeStampedModel):
    property = ForeignKey(Property, on_delete=SET_NULL, null=True, default=1, related_name="compareproperty")

    class Meta:
        managed = True
        verbose_name = "Property Compare"
        verbose_name_plural = "Properties Compared"
        ordering = ["-created"]


class PropertyBookmark(TimeStampedModel):
    user = ForeignKey(User, on_delete=CASCADE, related_name="bookmarkuser")
    property = ForeignKey(Property, on_delete=SET_NULL, null=True, related_name="bookmarkproperty")
    active = BooleanField(default=False)

    def __str__(self):
        return f"{self.user.fullname} Bookmarked {self.property.property_title}"

    def deleted_property(self):
        obj = Property.objects.filter(approved=True, property_sold=False, property_title=self.property.property_title).exits()
        if not obj:
            PropertyBookmark.objects.filter(property=self.property, user=self.user).delete()
            return True
        return False

    def sold_property(self):
        obj = Property.objects.filter(approved=True, property_sold=True, property_title=self.property.property_title).exits()
        if obj:
            PropertyBookmark.objects.filter(property=self.property, user=self.user, active=True).update(active=False)
            return True
        return False

    class Meta:
        managed = True
        verbose_name = "Property Bookmark"
        verbose_name_plural = "Properties Bookmarked"
        ordering = ["-created"]

class PropertySearchSaved(TimeStampedModel):
    user = ForeignKey(User, on_delete=CASCADE, related_name="searchuser")
    search_link = URLField(blank=True, null=True)
    saved = BooleanField(default=False)

    def __str__(self):
        return f"{self.user.fullname} saved {self.search_link}"

    class Meta:
        managed = True
        verbose_name = "Property Search Query"
        verbose_name_plural = "Properties Search Query"
        ordering = ["-created"]

        