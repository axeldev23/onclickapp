from django.core.management.base import BaseCommand
from prestamos.models import Prestamo, Pago
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Actualiza el estatus de todos los préstamos.'

    def handle(self, *args, **kwargs):
        hoy = now().date()
        prestamos = Prestamo.objects.all()

        for prestamo in prestamos:
            pagos_pendientes = Pago.objects.filter(prestamo=prestamo, pagado=False)

            if not pagos_pendientes.exists():
                estatus = 'A Tiempo'
            elif any(pago.fecha_pago_programada < hoy for pago in pagos_pendientes):
                estatus = 'Atrasado'
            else:
                estatus = 'A Tiempo'

            prestamo.estatus_pago = estatus
            prestamo.save()

        self.stdout.write(self.style.SUCCESS('Estatus de préstamos actualizado correctamente.'))
