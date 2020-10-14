from django.http.response import HttpResponse
from playthrough.models import Archive
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required(login_url='/login')
def serve_archive(request, filename):
    archive = get_object_or_404(Archive, file__exact=f'protected/{filename}')
    if archive.users.filter(id=request.user.id).exists():
        return HttpResponse("Unauthorized", status=403)

    response = HttpResponse()
    del response['Content-Type']
    response['X-Accel-Redirect'] = f'/protected/{filename}'
    return response
