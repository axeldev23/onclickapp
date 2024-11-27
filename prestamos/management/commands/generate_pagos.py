from django.core.management.base import BaseCommand
from datetime import timedelta
from prestamos.models import Prestamo, Pago

class Command(BaseCommand):
    help = 'Genera pagos para todos los préstamos existentes sin pagos'

    def handle(self, *args, **kwargs):
        prestamos = Prestamo.objects.all()

        for prestamo in prestamos:
            # Verifica si ya existen pagos para el préstamo
            if Pago.objects.filter(prestamo=prestamo).exists():
                self.stdout.write(f"Pagos ya existen para el préstamo ID {prestamo.id}")
                continue

            # Calcular el interés simple
            interes_simple = prestamo.monto_credito * (prestamo.interes / 100) if prestamo.interes else 0

            # Cálculo del monto total a pagar (monto crédito + interés simple)
            total_pagar = prestamo.monto_credito + interes_simple

            # Calcular el monto semanal
            monto_semanal = total_pagar / prestamo.plazo_credito

            # Generar los pagos pendientes semanales
            for i in range(prestamo.plazo_credito):
                fecha_programada = prestamo.fecha_primer_pago + timedelta(weeks=i)
                Pago.objects.create(
                    prestamo=prestamo,
                    fecha_pago_programada=fecha_programada,
                    monto_pago=round(monto_semanal, 2),
                    pagado=False
                )

            self.stdout.write(f"Pagos generados para el préstamo ID {prestamo.id}")
