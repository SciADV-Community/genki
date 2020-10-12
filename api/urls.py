from django.urls import path

from . import views

urlpatterns = [
    path('discord/callback', views.discord_callback, name='discord_callback'),
]
