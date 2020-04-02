from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def hello(request):
    return render(request, 'index.html', {
        'questions': range(10),
    })
# Create your views here.
