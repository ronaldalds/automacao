from django.contrib import admin
from .models import FaturamentoLog


@admin.register(FaturamentoLog)
class FaturamentoAdmin(admin.ModelAdmin):
    list_display = (
        "mk",
        "data_faturamento",
        "status",
        "observacao",
    )
    list_display_links = list_display
