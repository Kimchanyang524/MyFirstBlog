from django.shortcuts import render, redirect
from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreateView.as_view()
post_update = PostUpdateView.as_view()
post_delete = PostDeleteView.as_view()
