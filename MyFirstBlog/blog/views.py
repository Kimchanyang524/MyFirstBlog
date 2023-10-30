from django.shortcuts import render, redirect
from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse

from .models import Post, Comment
from .forms import PostForm, CommentForm

# django views
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    ordering = "-pk"


class PostDetail(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = "__all__"
    template_name = "blog/post_form.html"

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect("post_list")


class PostUpdateView(UpdateView):
    model = Post
    fields = "__all__"
    template_name = "blog/post_form.html"

    def post(self, request, pk):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.get(pk=pk)
            post.title = form.cleaned_data["title"]
            post.content = form.cleaned_data["content"]
            post.head_image = form.cleaned_data["head_image"]
            post.save()
        return redirect("post_list")


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")


post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreateView.as_view()
post_update = PostUpdateView.as_view()
post_delete = PostDeleteView.as_view()
