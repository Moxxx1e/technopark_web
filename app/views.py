from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from .models import *

gl_per_page = 10


def paginate(objects_list, request, per_page=gl_per_page):
    paginator = Paginator(objects_list, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    new_questions = Question.objects.new_questions()
    return render(request, 'index.html', {
        'number_of_questions': range(gl_per_page),
        'questions': new_questions,
        'page_obj': paginate(new_questions, request)
    })


def question(request, qid):
    question_, answers, ans_count = Question.objects.one_question(qid)
    return render(request, 'question.html', {
        'question': question_,
        'answers': answers,
        'ans_count': ans_count
    })


def tag(request, tag_):
    questions = Question.objects.tag_questions(tag_)
    return render(request, 'tag_questions.html', {
        'tag': tag_,
        'questions': questions,
        'page_obj': paginate(questions, request)
    })


def hot(request):
    questions = Question.objects.hot_questions()
    return render(request, 'hot.html', {
        'questions': questions,
        'page_obj': paginate(questions, request)
    })


def login(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def ask(request):
    return render(request, 'ask.html', {})
