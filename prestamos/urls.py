from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'prestamos', views.PrestamoViewSet)
router.register(r'clientes', views.ClienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='Prestamos API')),
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('profile', views.profile),

]
