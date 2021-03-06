from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),

    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('ask/', views.ask, name='ask'),

    path('question/<int:qid>/', views.question, name='question'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('logout/', views.logout_view, name='logout'),
    path('vote/', views.like_ajax, name='vote')
]
