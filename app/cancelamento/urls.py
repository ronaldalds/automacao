from django.urls import path, include
from .views import CancelamentoViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'cancelamentos', CancelamentoViewSet, basename='cancelamento')

urlpatterns = [
    path(
        "",
        include(router.urls)
    ),
]
