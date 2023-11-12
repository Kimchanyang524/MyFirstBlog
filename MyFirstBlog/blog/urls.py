from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("blog.post.urls")),
    path("<int:pk>/comment/", include("blog.comment.urls")),
    path("search/", include("blog.search.urls")),
    path("test", views.test),
]
