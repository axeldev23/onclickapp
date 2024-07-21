from rest_framework import serializers
from .models import Prestamo, Cliente
from django.contrib.auth.models import User


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    foto_identificacion = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Cliente
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

# FORMATO TABLA DE AMORTIZACIÓN
class DocumentSerializerAmortizacion(serializers.Serializer):
    nombre_completo = serializers.CharField(max_length=255)
    equipo_a_adquirir = serializers.CharField(max_length=255)
    equipo_precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    pago_inicial = serializers.DecimalField(max_digits=10, decimal_places=2)
    monto_credito = serializers.DecimalField(max_digits=10, decimal_places=2)
    plazo_credito = serializers.IntegerField()
    monto_parcialidad = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_a_pagar = serializers.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = serializers.DateField(format='%Y-%m-%d')
    imei = serializers.CharField()
    domicilio_actual = serializers.CharField()
    numero_telefono = serializers.CharField()
    prestamo_id = serializers.CharField()
    fecha_primer_pago = serializers.DateField(format='%Y-%m-%d')

# FORMATO PAGARÉ
class DocumentSerializer(serializers.Serializer):
    fecha_inicio = serializers.CharField()
    equipo_a_adquirir = serializers.CharField()
    interes = serializers.CharField()
    plazo_credito = serializers.CharField()
    nombre_completo = serializers.CharField()
    clave_elector = serializers.CharField()
    domicilio_actual = serializers.CharField()
    variable_total_a_pagar = serializers.CharField()
    variable_fecha_primer_pago = serializers.CharField()
    variable_fecha_ultimo_pago = serializers.CharField()


