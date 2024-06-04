from rest_framework import viewsets
from .models import Prestamo, Cliente
from .serializer import PrestamoSerializer, ClienteSerializer


# Create your views here.
class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

