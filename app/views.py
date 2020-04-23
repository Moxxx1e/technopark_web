from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from .models import *
from app import forms

gl_per_page = 10


def paginate(objects_list, request, per_page=gl_per_page):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    new_questions = Question.objects.new_questions()
    return render(request, 'index.html', {
        'questions': paginate(new_questions, request),
    })


def question(request, qid):
    question_, answers, ans_count = Question.objects.one_question(qid)
    return render(request, 'question.html', {
        'question': question_,
        'answers': answers,
        'ans_count': ans_count
    })


def tag(request, tag):
    questions = Question.objects.tag_questions(tag)
    return render(request, 'tag_questions.html', {
        'tag': tag,
        'questions': paginate(questions, request)
    })


def hot(request):
    questions = Question.objects.hot_questions()
    return render(request, 'hot.html', {
        'questions': paginate(questions, request),
    })


def login(request):
    if request == 'GET':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                print(form.errors)
                print(form.cleaned_data)
                auth.login(request, user)
                return redirect("/")  # TODO: correct redirect

    context = {'form': form}
    return render(request, 'login.html', context)


def signup(request):
    return render(request, 'signup.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def ask(request):
    return render(request, 'ask.html', {})
