from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator


def paginate(objects_list, request, per_page=10):
    #do smth with Paginator, etc...
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)
    objects_page = paginator.get_page(page)
    return objects_page
    
questions = []
for i in range(1, 30):
    questions.append({
        'title': 'title' + str(i),
        'id': i,
        'text': 'text' + str(i)
    })

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

def question(request, qid):
    question = questions[qid]
    return render(request, 'question.html', {
        'question': question 
    })

def tag(request, tag):
    return render(request, 'tag_questions.html', {
        'tag': tag,
        'questions': range(10),
    }
)

def hot(request):
    return render(request, 'hot.html', {
        'questions': range(5)
    })
