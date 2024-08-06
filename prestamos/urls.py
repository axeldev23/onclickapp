from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'prestamos', views.PrestamoViewSet)
router.register(r'clientes', views.ClienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='Prestamos API')),
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('profile', views.profile),
    path('download_image/<int:cliente_id>/', views.download_image, name='download_image'),  # Añade esta línea
    path('clientes/<int:cliente_id>/update/', views.update_cliente, name='update_cliente'),
    path('generar-pagare/', views.DocumentAPIView.as_view(), name='generar-pagare'),  # Asegúrate de que esta línea esté correcta
    path('generar-contrato/', views.AmortizacionAPIView.as_view(), name='generar-contrato'),  # Asegúrate de que esta línea esté correcta
    path('get_user_by_id/', views.get_user_by_id, name='get_user_by_id'),  # Añade esta línea


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)