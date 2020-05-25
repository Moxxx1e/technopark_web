from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
        'paginate_objects': paginate(new_questions, request),
        'questions': paginate(new_questions, request),
    })


def question(request, qid):
    question_, answers, ans_count = Question.objects.one_question(qid)

    if request.method == "GET":
        form = forms.AnswerForm(request.user, question_)
        context = {'question': question_, 'answers': answers,
                   'paginate_objects': paginate(answers, request),
                   'ans_count': ans_count,
                   'form': form}
        return render(request, 'question.html', context)

    # TODO: change user to user.profile
    form = forms.AnswerForm(request.user, question_, request.POST)
    if form.is_valid():
        answer = form.save()
        return redirect(reverse('question', kwargs={'qid': qid}))

    context = {'question': question_, 'answers': answers,
               'paginate_objects': paginate(answers, request),
               'ans_count': ans_count,
               'form': form}
    return render(request, 'question.html', context)


def tag(request, tag):
    questions = Question.objects.tag_questions(tag)
    return render(request, 'tag_questions.html', {
        'tag': tag,
        'paginate_objects': paginate(questions, request),
        'questions': paginate(questions, request)
    })


def hot(request):
    questions = Question.objects.hot_questions()
    return render(request, 'hot.html', {
        'questions': paginate(questions, request),
        'paginate_objects': paginate(questions, request),
    })


def login(request):
    if request.method == 'GET':
        form = forms.LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    form = forms.LoginForm(data=request.POST)
    if form.is_valid():
        user = auth.authenticate(request, **form.cleaned_data)
        if user is not None:
            auth.login(request, user)
            return redirect("/")  # TODO: correct redirect

    context = {'form': form}
    return render(request, 'login.html', context)


def signup(request):
    if request.method == 'GET':
        form = forms.SignupForm()
        context = {'form': form}
        return render(request, 'signup.html', context)

    form = forms.SignupForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        user, profile = form.save()
        auth.login(request, user)
        return redirect("/ask")

    context = {'form': form}
    return render(request, 'signup.html', context)


def settings(request):
    return render(request, 'settings.html', {})


@login_required
def ask(request):
    if request.method == "GET":
        form = forms.QuestionForm(request.user)
        context = {'form': form}
        return render(request, 'ask.html', context)

    #TODO: change user to user.profile
    form = forms.QuestionForm(request.user, request.POST)
    if form.is_valid():
        question = form.save()
        return redirect(reverse('question', kwargs={'qid': question.id}))

    context = {'form': form}
    return render(request, 'ask.html', context)
