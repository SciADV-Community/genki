import requests
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login


def discord_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({
            'error': 'Code not provided.'
        }, status=500)
    data = {
        'client_id': settings.DISCORD_CLIENT_ID,
        'client_secret': settings.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': request.build_absolute_uri(reverse('api:discord_callback')),
        'scope': 'identify',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    response_payload = r.json()
    access_token = response_payload['access_token']
    user_data = requests.get('https://discord.com/api/v6/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    }).json()
    user = authenticate(request, user_info=user_data)
    login(request, user)
    return redirect(reverse('terminal:archives'))
