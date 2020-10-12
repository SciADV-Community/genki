from urllib.parse import quote_plus
from django.http.response import JsonResponse

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'terminal/index.html')


def login(request):
    CLIENT_ID = settings.DISCORD_CLIENT_ID
    _redirect = quote_plus(request.build_absolute_uri(reverse('api:discord_callback')))

    return redirect((
        f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&'
        f'redirect_uri={_redirect}&response_type=code&scope=identify'
    ))


@login_required(login_url='/login')
def archives(request):
    return JsonResponse({
        "id": request.user.id,
        "name": request.user.username
    })
