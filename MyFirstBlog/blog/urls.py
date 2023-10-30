from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("write/", views.post_create, name="post_create"),
    path("edit/<int:pk>/", views.post_update, name="post_update"),
    path("delete/<int:pk>", views.post_delete, name="post_delete"),
]
