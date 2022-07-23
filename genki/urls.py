"""genki URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from playthrough import views

urlpatterns = [
    path("", include("terminal.urls")),
    path("api/", include("api.urls", namespace="api")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
else:
    urlpatterns.append(
        path(
            "media/protected/<path:filename>", views.serve_archive, name="serve_archive"
        )
    )
