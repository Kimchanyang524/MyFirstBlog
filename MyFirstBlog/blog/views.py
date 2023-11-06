from django.shortcuts import render, redirect, get_object_or_404
from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse, Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

# custom .py
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

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

pageslice = 30


class PostList(ListView):
    model = Post
    ordering = "-pk"
    context_object_name = "posts"
    paginate_by = pageslice


class PostSearch(ListView):
    model = Post
    ordering = "-pk"
    context_object_name = "posts"
    paginate_by = pageslice

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return queryset


class PostSearchTag(ListView):
    model = Post
    ordering = "-pk"
    context_object_name = "posts"
    paginate_by = pageslice

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.kwargs["tag"]
        queryset = queryset.filter(tags__name=tag)
        return queryset


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return render(request, "blog/post_404.html")
        post.view_count += 1
        post.save()
        try:
            next_post = (
                Post.objects.filter(created_at__gt=post.created_at)
                .order_by("created_at")
                .first()
            )
        except Post.DoesNotExist:
            next_post = None

        try:
            previous_post = (
                Post.objects.filter(created_at__lt=post.created_at)
                .order_by("-created_at")
                .first()
            )
        except Post.DoesNotExist:
            previous_post = None
        comments = Comment.objects.filter(post=post)
        contaxt = {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
            "comments": comments,
        }
        return render(request, "blog/post_detail.html", contaxt)

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return render(request, "blog/post_404.html")
        try:
            next_post = (
                Post.objects.filter(created_at__gt=post.created_at)
                .order_by("created_at")
                .first()
            )
        except Post.DoesNotExist:
            next_post = None

        try:
            previous_post = (
                Post.objects.filter(created_at__lt=post.created_at)
                .order_by("-created_at")
                .first()
            )
        except Post.DoesNotExist:
            previous_post = None
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        comments = Comment.objects.filter(post=post)
        contaxt = {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
            "comments": comments,
        }
        return render(request, "blog/post_detail.html", contaxt)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
        return redirect("post_list")


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = "__all__"
    template_name = "blog/post_form.html"

    def test_func(self):
        """
        이 메서드에서 사용자의 권한을 확인
        """
        post = self.get_object()  # 업데이트할 게시물 가져오기
        return self.request.user == post.author  # 사용자가 게시물의 작성자인지 확인

    def handle_no_permission(self):
        """
        사용자가 권한이 없는 경우 처리할 동작 정의

        예를 들어, 권한이 없을 때 리디렉션하거나 오류 메시지를 표시할 수 있음
        """
        messages.error(self.request, "글쓴이가 아닙니다.")
        return super().handle_no_permission()

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
