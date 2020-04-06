from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
from .models import *

gl_per_page = 10

# for nav bar view:
'''
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
'''

def paginate(objects_list, request, per_page=gl_per_page):
    paginator = Paginator(objects_list, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

#questions = Question.objects.all()
new_questions = Question.objects.new_questions()
'''
questions = []
for i in range(1, 31):
    questions.append({
        'title': 'title' + str(i),
        'id': i,
        'text': 'text' + str(i)
    })
'''

def index(request):
    return render(request, 'index.html', {
        'number_of_questions': range(gl_per_page),
        'questions': new_questions,
        'page_obj': paginate(new_questions, request)
    })

def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def ask(request):
    return render(request, 'ask.html', {})

def question(request, qid):
    question = new_questions[qid - 1]
    return render(request, 'question.html', {
        'question': question,
        'answers': range(3),
    })

def tag(request, tag):
    questions = Question.objects.tag_questions(tag)
    return render(request, 'tag_questions.html', {
        'tag': tag,
        'questions': questions,
        'page_obj': paginate(questions, request)
    }
)

def hot(request):
    questions = Question.objects.hot_questions()
    return render(request, 'hot.html', {
        'questions': questions,
        'page_obj': paginate(questions, request)
    })
