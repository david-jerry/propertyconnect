from django.urls import path

from afriproperty.users.views import (
    AgentCompanyListView,
    AgentCompanyView,
    AgentDetailView,
    AgentListView,
    AgentProperties,
    AgentSearchView,
    UserBookmarks,
    user_detail_view,
    user_notification_view,
    user_profile_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~search/", view=AgentSearchView.as_view(), name="search"),
    path("~update/", view=user_update_view, name="update"),
    path("~notifications/", view=user_notification_view, name="notification"),
    path("~agents/", view=AgentListView.as_view(), name="agents"),
    path("~agent/<slug>/", view=AgentDetailView.as_view(), name="agent"),
    path("~companies/", view=AgentCompanyListView.as_view(), name="companies"),
    path("~company/<slug>/", view=AgentCompanyView.as_view(), name="company"),
    path("agent/properties/", view=AgentProperties.as_view(), name="properties"),
    path("~profile/", view=user_profile_view, name="profile"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/~bookmarks/", view=UserBookmarks.as_view(), name="bookmarks"),
]
