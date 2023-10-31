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
    model = User
    form_class = UserForm
    template_name = "accounts/register.html"

    def post(self, request):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("post_list")


class MyLoginView(LoginView):
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

    template_name = "accounts/login.html"
    success_url = "post_list"


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
