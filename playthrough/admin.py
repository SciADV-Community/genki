from django.contrib import admin
from playthrough.models import (
    Channel, GameConfig, Guild, Archive, Alias, Game, Series,
    User, MetaRoleConfig, RoleTemplate
)
from django.contrib.contenttypes.admin import GenericTabularInline


class AliasInline(GenericTabularInline):
    model = Alias
    extra = 0


class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [AliasInline]


class ArchiveInline(admin.TabularInline):
    model = Archive
    extra = 0


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    inlines = [ArchiveInline]


class GameConfigInline(admin.TabularInline):
    model = GameConfig
    extra = 0


class MetaRoleConfigInline(admin.TabularInline):
    model = MetaRoleConfig
    extra = 0


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    inlines = [GameConfigInline, MetaRoleConfigInline]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ChannelInline]


# Register your models here.
admin.site.register(Archive)
admin.site.register(RoleTemplate)
admin.site.register(Series)
