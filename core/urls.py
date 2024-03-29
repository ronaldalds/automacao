"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import cronos_admin_login, ValidateTokenView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Técnico Online",
        default_version='v1',
        description="API para automações",
        contact=openapi.Contact(email="ronald.ralds@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path(
        'admin/login/',
        cronos_admin_login
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'token/',
        ValidateTokenView.as_view(),
        name='validate_token',
    ),
    path(
        'api-auth/',
        obtain_auth_token,
        name='api_auth'
    ),
    # path(
    #     "dashboards/",
    #     include("app.dashboard.urls")
    # ),
    # path(
    #     "watch/",
    #     include("app.watch.urls")
    # ),
    # path(
    #     "movimentacoes/",
    #     include("app.movimentacao.urls")
    # ),
    # path(
    #     "ost-tecnicos/",
    #     include("app.ost.tecnico_urls")
    # ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
