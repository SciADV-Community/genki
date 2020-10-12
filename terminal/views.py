from urllib import quote_plus

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


def login(request):
    CLIENT_ID = settings.DISCORD_CLIENT_ID
    _redirect = quote_plus(reverse('api:discord_callback'))
    return redirect(request, (
        f'https://discordapp.com/api/oauth2/authorize?client_id={CLIENT_ID}&'
        f'scope=identify&response_type=code&redirect_uri={_redirect}'
    ))
