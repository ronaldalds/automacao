from django.urls import path
from .views import CancelamentoViewSet


urlpatterns = [
    path(
        "cancelar/",
        CancelamentoViewSet.as_view({"post": "cancelar"})
    ),
    path(
        "parar/",
        CancelamentoViewSet.as_view({"post": "parar_cancelamento"})
    ),
]
