import requests
from requests.auth import HTTPBasicAuth
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


def discord_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({
            'error': 'Code not provided.'
        }, status=500)
    auth_token_url = (
        'https://discordapp.com/api/oauth2/token?'
        f'grant_type=authorization_code&code=${code}'
    )
    r = requests.post(auth_token_url, auth=HTTPBasicAuth(
        settings.DISCORD_CLIENT_ID, settings.DISCORD_CLIENT_SECRET
    ))
    response_payload = r.json()
    access_token = response_payload['access_token']
    return redirect(reverse('terminal:archives'))
