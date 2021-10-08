from django.urls import path

from .api import (
    add_bookmark_api,
    add_property_compare,
    mark_property_purchased,
    mark_property_sold,
    property_delete,
    remove_bookmark_api,
    remove_property_compare,
)
from .views import (  # mapJson,
    PropertyCompareListView,
    PropertyDetailView,
    PropertyListView,
    PropertyMapListView,
    PropertySearchListview,
    property_create_view,
    property_update_view,
)

app_name = "property"
urlpatterns = [
    path("", view=PropertyListView.as_view(), name="list"),
    path("update/", view=property_update_view, name="update"),
    path("create/", view=property_create_view, name="create"),
    path("compare/", view=PropertyCompareListView.as_view(), name="compare"),
    path("search/", view=PropertySearchListview.as_view(), name="search"),
    path("mapped/", view=PropertyMapListView.as_view(), name="map"),
    path("<slug>/", view=PropertyDetailView.as_view(), name="detail"),

    # Ajax request with vuejs
    path("api/sold/", view=mark_property_sold, name="sold"),
    path("api/purchased/", view=mark_property_purchased, name="purchased"),
    path("api/deleted/", view=property_delete, name="delete"),
    path("add/bookmark/", view=add_bookmark_api, name="add_bookmark"),
    path("remove/bookmark/", view=remove_bookmark_api, name="remove_bookmark"),
    path("add/compare/", view=add_property_compare, name="add_compare"),
    path("remove/compare/", view=remove_property_compare, name="remove_compare"),
]
