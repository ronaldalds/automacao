from django.contrib import admin
from reversion.admin import VersionAdmin
from import_export.admin import ImportExportMixin
from .models import (
    Login,
    TipoOS,
    Profile,
)


# Register your models here.
@admin.register(Login)
class LoginAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'url',
        'username',
    )
    list_display_links = list_display


@admin.register(TipoOS)
class TipoOSAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'id_web',
        'mk',
        'descricao',
    )
    list_display_links = list_display


@admin.register(Profile)
class ProfileAdmin(ImportExportMixin, VersionAdmin):
    list_display = (
        'id',
        'id_web',
        'mk',
        'descricao',
    )
    list_display_links = list_display
