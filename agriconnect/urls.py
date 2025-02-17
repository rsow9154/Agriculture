from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuration de la vue Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Agriconnect API",
        default_version='v1',
        description="API pour la gestion des produits et commandes agricoles.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@agriconnect.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Rediriger la racine vers Swagger
    path('', RedirectView.as_view(url='/swagger/', permanent=True)),

    # Routes de l'API
    path('api/', include('api.urls')),

    # Documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Documentation ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]