from django.contrib import admin
from .models import UserMkat


@admin.register(UserMkat)
class UserMkatAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'token')
    search_fields = ['nome',]