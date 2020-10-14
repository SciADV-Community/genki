from django.urls import path

from . import views

app_name = 'terminal'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('archives', views.archives, name='archives'),
    path('archives/<int:archive_id>/delete', views.delete_archive, name='delete_archive'),
]
