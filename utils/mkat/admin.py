from django.contrib.admin import ModelAdmin, register
from .models import UserMkat


@register(UserMkat)
class UserMkatAdmin(ModelAdmin):
    list_display = ('id', 'nome', 'token')
    search_fields = ['nome',]