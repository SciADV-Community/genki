from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('discord/callback', views.discord_callback, name='discord_callback'),
]
