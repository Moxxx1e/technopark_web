from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request):
    return render(request, 'index.html', {
        'questions': range(10),
    })

def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def ask(request):
    return render(request, 'ask.html', {})

def question_page(request):
    return render(request, 'question_page.html', {
        'answers': range(3)
    })

def tag(request):
    return render(request, 'tag_questions.html', {
        'tag': 'bender',
        'questions': range(10),
    }
)


    