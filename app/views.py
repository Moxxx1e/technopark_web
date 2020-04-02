from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def hello(request):
    return HttpResponse('foo')
# Create your views here.
