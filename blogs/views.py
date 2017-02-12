from django.shortcuts import render

from .forms import UserForm

# Create your views here.


def index(request):
    return render(request, "blogs/index.html", {})
