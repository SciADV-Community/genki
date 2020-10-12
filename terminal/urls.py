from django.urls import path

from . import views

app_name = 'terminal'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('archives', views.archives, name='archives'),
]
