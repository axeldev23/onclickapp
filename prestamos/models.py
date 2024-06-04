from django.db import models

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    domicilio_actual = models.CharField(max_length=255)
    correo_electronico = models.EmailField(blank=True, null=True)
    numero_telefono = models.CharField(max_length=20)
    foto_identificacion = models.ImageField(upload_to='clientes_identificaciones/', blank=True, null=True)

    def __str__(self):
        return self.nombre_completo

class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cambiar cliente_id a cliente
    imei = models.CharField(max_length=255)
    equipo_a_adquirir = models.CharField(max_length=255)
    equipo_precio = models.DecimalField(max_digits=10, decimal_places=2)
    monto_credito = models.DecimalField(max_digits=10, decimal_places=2)
    plazo_credito = models.IntegerField()
    pago_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=100, default='ACTIVO')

    def __str__(self):
        return f"{self.cliente.nombre_completo} - {self.equipo_a_adquirir}"
