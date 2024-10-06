from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns, set_language


schema_view = get_schema_view(
    openapi.Info(
        title="Davr auto-service API",
        default_version='v1',
        description="Korxonadagi kirim-chiqimlar, har bir jarayonlarni aniqlik bilan saqlab, "
                    "shu jarayonlar va korxona statistikasini kuzata olish imkoniyatlari.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="cbekoder@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user/', include('users.urls')),
    path('inventory/', include('inventory.urls')),
    path('service/', include('services.urls')),
    path('transaction/', include('transactions.urls')),
    path('set_language/', set_language, name='set_language'),
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    ]
