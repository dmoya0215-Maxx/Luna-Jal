"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from api import views
from sistema.error_views import (
    error_404,
    view_error_400,
    view_error_403,
    view_error_404,
    view_error_500,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Handlers de error personalizados
handler400 = 'sistema.error_views.error_400'
handler403 = 'sistema.error_views.error_403'
handler404 = 'sistema.error_views.error_404'
handler500 = 'sistema.error_views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Previsualización de páginas de error (solo desarrollo o admin)
    path('errores/400/', view_error_400, name='error_preview_400'),
    path('errores/403/', view_error_403, name='error_preview_403'),
    path('errores/404/', view_error_404, name='error_preview_404'),
    path('errores/500/', view_error_500, name='error_preview_500'),

    path('', include('user.urls')),
    path('', include('people.urls')),
    path('', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('api/auth/', include('rest_framework.urls')),

     # Documentación OpenAPI
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

     # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),

    # ReDoc
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(
            url_name='schema'
        ),
        name='redoc'
    ),

    # Comodín final: cualquier URL no coincidente -> vista 404 personalizada
    re_path(r'^.*', error_404, name='error_404_catchall'),
]
