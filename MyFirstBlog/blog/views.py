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
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    pass


class PostDetail(DetailView):
    pass


postlist = PostList.as_view()
postdetail = PostDetail.as_view()
