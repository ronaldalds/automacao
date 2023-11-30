from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'tecnico', TecnicoViewSet)
router.register(r'tipo', TipoOSViewSet)
router.register(r'sla', TempoSLAViewSet)
# router.register(r'sla_os', SLA_OSViewSet)
# router.register(r'mensagem', TecnicosMensagemViewSet)
router.register(r'informacao', InformacaoOSViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
