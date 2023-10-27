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


post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreateView.as_view()


def select5(request):
    return Post.objects.last()
