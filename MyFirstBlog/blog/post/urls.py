from django.urls import path, include
from blog import views

app_name = "post"

urlpatterns = [
    path("", views.PostList.as_view(), name="list"),
    path("<int:pk>/", views.PostDetail.as_view(), name="detail"),
    path("write/", views.PostCreateView.as_view(), name="create"),
    path("edit/<int:pk>/", views.PostUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.PostDeleteView.as_view(), name="delete"),
]
