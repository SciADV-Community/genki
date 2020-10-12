from django.http.response import FileResponse, HttpResponse
from playthrough.models import Archive
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required(login_url='/login')
def serve_archive(request, filename):
    archive = get_object_or_404(Archive, file__path=f'protected/{filename}')
    if request.user not in Archive:
        return HttpResponse("Unauthorized", status=403)

    response = HttpResponse()
    response['Content-Disposition'] = f'attachment; filename={archive.file.name}'
    response['X-Accel-Redirect'] = archive.file.name
    return response
