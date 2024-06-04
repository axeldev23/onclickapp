from django.contrib import admin
from .models import Prestamo, Cliente

# Register your models here.
admin.site.register(Prestamo)
admin.site.register(Cliente)