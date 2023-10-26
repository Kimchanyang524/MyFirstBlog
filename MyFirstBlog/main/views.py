from django.shortcuts import render

# costom.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    return render(request, "main/index.html")
