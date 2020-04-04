from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator

gl_per_page = 10

def paginate(objects_list, request, per_page=gl_per_page):
    paginator = Paginator(objects_list, per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

questions = []
for i in range(1, 31):
    questions.append({
        'title': 'title' + str(i),
        'id': i,
        'text': 'text' + str(i)
    })

def index(request):
    return render(request, 'index.html', {
        'questions': range(gl_per_page),
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

def question(request, qid):
    question = questions[qid - 1]
    return render(request, 'question.html', {
        'question': question 
    })

def tag(request, tag):
    return render(request, 'tag_questions.html', {
        'tag': tag,
        'questions': range(gl_per_page),
        'page_obj': paginate(questions, request)
    }
)

def hot(request):
    return render(request, 'hot.html', {
        'questions': range(gl_per_page),
        'page_obj': paginate(questions, request)
    })
