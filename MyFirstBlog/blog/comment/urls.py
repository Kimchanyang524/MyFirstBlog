from django.urls import path, include
from .. import views

app_name = "comment"

urlpatterns = [
    path("", views.PostList.as_view(), name="update"),
]