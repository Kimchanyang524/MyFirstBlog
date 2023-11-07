from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path("<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
    path("search/", views.PostSearch.as_view(), name="post_search"),
    path("search/<str:tag>/", views.PostSearchTag.as_view(), name="post_search_tag"),
    path("write/", views.PostCreateView.as_view(), name="post_create"),
    path("edit/<int:pk>/", views.PostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>", views.PostDeleteView.as_view(), name="post_delete"),
    path("test", views.test),
]
