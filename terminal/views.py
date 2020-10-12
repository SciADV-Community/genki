from urllib.parse import quote_plus
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponse

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as user_logout

from playthrough.models import Archive, Channel


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('terminal:archives'))
    return render(request, 'terminal/index.html')


def login(request):
    CLIENT_ID = settings.DISCORD_CLIENT_ID
    _redirect = quote_plus(request.build_absolute_uri(reverse('api:discord_callback')))

    return redirect((
        f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&'
        f'redirect_uri={_redirect}&response_type=code&scope=identify'
    ))


def logout(request):
    user_logout(request)
    return redirect(reverse('terminal:index'))


@login_required(login_url='/login')
def archives(request):
    _channels = Channel.objects.exclude(archives=None)\
        .select_related('game', 'game__series', 'guild')\
        .prefetch_related('archives').filter(
            Q(archives__users__in=[request.user]) | Q(owner=request.user)
        ).distinct()
    return render(request, 'terminal/archives.html', context={
        'channels': _channels
    })


@login_required(login_url='/login')
def delete_archive(request, archive_id):
    try:
        archive = Archive.objects.select_related('channel').get(pk=archive_id)
    except Archive.DoesNotExist:
        raise Http404("Archive does not exist.")
    if request.user.id != archive.channel.owner_id:
        return HttpResponse("Unauthorized", status=403)
    archive.delete()
    return redirect(reverse('terminal:archives'))
