from django.shortcuts import render

# Create your views here.

from django.http import Http404


def index(request):
    return Http404("你来到了知识的荒原...")
