from django.shortcuts import render, redirect

# costom.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    return redirect("post_list")
