from django.db import models
import os
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone





class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    domicilio_actual = models.CharField(max_length=255)
    correo_electronico = models.EmailField(blank=True, null=True)
    numero_telefono = models.CharField(max_length=20)
    foto_identificacion = models.ImageField(upload_to='clientes_identificaciones/', blank=True, null=True)
    clave_elector = models.CharField(max_length=18, unique=True)

    def delete(self, *args, **kwargs):
        if self.foto_identificacion:
            if default_storage.exists(self.foto_identificacion.name):
                default_storage.delete(self.foto_identificacion.name)
        super(Cliente, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            old_instance = Cliente.objects.get(pk=self.pk)
            if old_instance.foto_identificacion and old_instance.foto_identificacion != self.foto_identificacion:
                if default_storage.exists(old_instance.foto_identificacion.name):
                    default_storage.delete(old_instance.foto_identificacion.name)
        except Cliente.DoesNotExist:
            pass
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_completo

    
    
class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relacionado con cliente
    imei = models.CharField(max_length=255)
    equipo_a_adquirir = models.CharField(max_length=255)
    equipo_precio = models.DecimalField(max_digits=10, decimal_places=2)
    monto_credito = models.DecimalField(max_digits=10, decimal_places=2)
    plazo_credito = models.IntegerField()  # Número de pagos (semanales)
    pago_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Interés en porcentaje
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=100, default='ACTIVO')
    fecha_primer_pago = models.DateField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Nuevo campo estatus_pago
    ESTATUS_CHOICES = [
        ('A Tiempo', 'A Tiempo'),
        ('Atrasado', 'Atrasado'),
    ]
    estatus_pago = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default='A Tiempo', blank=True, null=True)

    def save(self, *args, **kwargs):
    # Si el préstamo ya existe, no volver a generar pagos
        if not self.pk:  # Esto indica que el préstamo es nuevo
            super(Prestamo, self).save(*args, **kwargs)  # Guardamos el préstamo primero
            
            # Cálculo del interés simple
            interes_simple = self.monto_credito * (self.interes / 100) if self.interes else 0
            
            # Cálculo del monto total a pagar (monto crédito + interés simple)
            total_pagar = self.monto_credito + interes_simple
            
            # Calcular el monto semanal
            monto_semanal = total_pagar / self.plazo_credito
            
            # Generar los pagos pendientes semanales
            for i in range(self.plazo_credito):
                fecha_programada = self.fecha_primer_pago + timedelta(weeks=i)  # Pagos semanales
                Pago.objects.create(
                    prestamo=self,
                    fecha_pago_programada=fecha_programada,
                    monto_pago=monto_semanal,
                    pagado=False
                )
        else:
            super(Prestamo, self).save(*args, **kwargs)  # Para actualizaciones, no se generan pagos nuevos


    def __str__(self):
        return f"{self.cliente.nombre_completo} - {self.equipo_a_adquirir}"



class Pago(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)  # Relaciona el pago con un préstamo específico
    fecha_pago_programada = models.DateField()  # Fecha en que se espera el pago
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del pago
    pagado = models.BooleanField(default=False)  # Indica si el pago ha sido realizado

    def __str__(self):
        return f"Pago {self.id} - {self.prestamo.cliente.nombre_completo} - {self.prestamo.equipo_a_adquirir}"
