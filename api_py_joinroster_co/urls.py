from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='https://app.joinroster.co/logo.png')),
    path('admin/', admin.site.urls),
    path('api/', include('roster_api.urls')),
    # OpenAPI Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
