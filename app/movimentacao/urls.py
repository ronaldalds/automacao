from django.urls import path, include
from .views import MovimentacaoViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'movimentacoes', MovimentacaoViewSet, basename='movimentacao')

urlpatterns = [
    path(
        "",
        include(router.urls)
    ),
]
