from django.contrib import admin
from playthrough.models import (
    Channel, Guild, Archive, Alias, RoleTemplate, Game, Series,
    User
)


class ArchiveInline(admin.TabularInline):
    model = Archive


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    inlines = [ArchiveInline]


# Register your models here.
admin.site.register(Guild)
admin.site.register(Archive)
admin.site.register(Alias)
admin.site.register(RoleTemplate)
admin.site.register(Series)
admin.site.register(Game)
admin.site.register(User)
