from django.urls import path, include
from .. import views

app_name = "search"

urlpatterns = [
    path("", views.PostSearch.as_view(), name="search"),
    path("<str:tag>/", views.PostSearchTag.as_view(), name="tag"),
]
