from django.shortcuts import render, redirect
from django.views.generic import ListView
from blog.models import Post, Tag

# Create your views here.


class PostPick6(ListView):
    model = Post
    ordering = "-pk"
    template_name = "main/index.html"

    def get_queryset(self):
        return Post.objects.all().order_by("-pk")[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


index = PostPick6.as_view()
