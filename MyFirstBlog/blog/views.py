from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

# custom .py
from .models import Post, Comment, Tag
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


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
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect("post_detail", pk=pk)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    context_object_name = "post"

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
            if form.cleaned_data["head_image"]:
                post.head_image = form.cleaned_data["head_image"]
            post.tags.set(form.cleaned_data["tags"])
            post.save()
        return redirect("post_list")


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")


def test(request):
    """
    테스트용 더미 데이터 생성함수

    현재 로그인된 사용자 기준으로 입력됨

    예외처리는 하지 않앗으니 주의해서 사용
    """
    tags = ["한식", "중식", "일식", "양식", "집밥", "외식", "간편식"]
    for i in range(1, 100):
        title = f"{i}번글"
        content = f"{i}번 내용"
        tag, created = Tag.objects.get_or_create(name=tags[i % 7])
        post = Post.objects.create(title=title, content=content, author=request.user)
        post.tags.add(tag)
        post.save()
    return redirect("post_list")
