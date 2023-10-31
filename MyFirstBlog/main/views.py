from django.shortcuts import render, redirect
from django.views.generic import ListView
from blog.models import Post

# Create your views here.


class PostPick6(ListView):
    model = Post
    ordering = "-pk"
    template_name = "main/index.html"

    def get_queryset(self):
        return Post.objects.all()[:6]


index = PostPick6.as_view()
