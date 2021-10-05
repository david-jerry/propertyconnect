from django.urls import path

from afriproperty.tips.views import TipDetailView, TipListView

app_name = "tips"
urlpatterns = [
    path("", view=TipListView.as_view(), name="list"),
    path("<slug>/", view=TipDetailView.as_view(), name="detail"),
]
