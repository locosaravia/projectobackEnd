# templatesApp/models.py

from django.db import models

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    contacto = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Bus(models.Model):
    patente = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=100)
    año = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return self.patente


class EstadoBus(models.Model):
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bus.patente} - {self.estado}"


class AsignacionRol(models.Model):
    trabajador_nombre = models.CharField(max_length=100)
    trabajador_apellido = models.CharField(max_length=100)
    rol_nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.trabajador_nombre} {self.trabajador_apellido} → {self.rol_nombre}"



class AsignacionBus(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trabajador} → {self.bus}"
