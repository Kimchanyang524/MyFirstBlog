from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.urls import reverse_lazy

# class view
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView

# mixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# costom .py
from .models import User
from .forms import UserForm


class MyRegister(CreateView):
    """
    회원가입을 시켜주는 클래스

    사용자의 정보를 받아서 User테이블에 정보를 추가하고
    블로그 글 목록으로 이동시키는 클래스입니다.

    Args:
        id: 아이디
        password: 비밀번호
        email: 이메일
        nickname: 닉네임
        profile_img: 프로필 이미지

    Raises:
        LogoutRequiredError: 이 클래스는 로그아웃을 요구한다.

    Returns:
        GET-None
        POST-redirect("post_list"): post_list로 즉시 이동시켜줍니다.
    """

    model = User
    form_class = UserForm
    template_name = "accounts/register.html"

    def post(self, request):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("post_list")


class MyLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = "post_list"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            html = """
                    <script>
                        alert('이미 로그인한 사용자입니다.')
                        window.location.href = "/blog/"
                    </script>
                    """
            return HttpResponse(html)
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        html = """
            <script>
                alert('로그인에 실패했습니다. 회원가입해주세요.');
                window.location.href = "/accounts/register";
            </script>
        """
        return HttpResponse(html)


class MyLogoutView(LoginRequiredMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            html = """
                    <script>
                        alert('로그인해야합니다.')
                        window.location.href = "/accounts/login"
                    </script>
                    """
            return HttpResponse(html)
        else:
            return super().dispatch(request, *args, **kwargs)

    next_page = "login"


login = MyLoginView.as_view()
logout = MyLogoutView.as_view()
register = MyRegister.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
