"""pruebaEON URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from acme.urls import ACME_URLS

SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title='Documentacion de Endpoints de ACME',
        default_version='v1',
        description='Documento que contiene los endpoints de ACME'
    ),
    public=True,
    permission_classes=(AllowAny,)

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', SCHEMA_VIEW.with_ui('swagger')),
    path('', include(ACME_URLS))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
