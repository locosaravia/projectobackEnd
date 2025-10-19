
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError

class Trabajador(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Solo se permiten letras')]
    )
    apellido = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Solo se permiten letras')]
    )
    direccion = models.CharField(max_length=255)
    contacto = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^\+?[0-9\s\-]+$', 'Formato de contacto inválido')]
    )
    edad = models.PositiveIntegerField(
        validators=[MinValueValidator(18, 'Debe ser mayor de 18 años'), 
                   MaxValueValidator(70, 'Edad máxima 70 años')]
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['apellido', 'nombre']

def clean(self):
    if self.edad and self.edad < 18:
        raise ValidationError('Trabajador debe ser mayor de 18 años')
    if self.nombre and self.apellido:
        if self.nombre.lower() == self.apellido.lower():
            raise ValidationError('El nombre y apellido no pueden ser iguales')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Rol(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'Solo se permiten letras')]
    )
    descripcion = models.TextField(blank=True, null=True)
    nivel_acceso = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Bus(models.Model):
    patente = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9\-]+$', 'Formato de patente inválido')]
    )
    modelo = models.CharField(max_length=100)
    año = models.PositiveIntegerField(
        validators=[MinValueValidator(1990, 'Año mínimo 1990'), 
                   MaxValueValidator(2025, 'Año máximo 2025')]
    )
    capacidad = models.PositiveIntegerField(
        validators=[MinValueValidator(10, 'Capacidad mínima 10 pasajeros'),
                   MaxValueValidator(80, 'Capacidad máxima 80 pasajeros')]
    )
    marca = models.CharField(max_length=100, default='Sin especificar')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"
        ordering = ['patente']

    def clean(self):
        if self.año > 2025:
            raise ValidationError('El año no puede ser futuro')

    def __str__(self):
        return f"{self.patente} - {self.modelo}"


class EstadoBus(models.Model):
    ESTADOS_CHOICES = [
        ('OPERATIVO', 'Operativo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('REPARACION', 'En Reparación'),
        ('FUERA_SERVICIO', 'Fuera de Servicio'),
        ('RESERVADO', 'Reservado'),
    ]

    bus_patente = models.CharField(max_length=20, unique=True)
    bus_modelo = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, default='OPERATIVO')
    observaciones = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now=True)
    kilometraje = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Estado de Bus"
        verbose_name_plural = "Estados de Buses"
        ordering = ['-fecha_cambio']

    def clean(self):
        if self.kilometraje < 0:
            raise ValidationError('El kilometraje no puede ser negativo')

    def __str__(self):
        return f"{self.bus_patente} - {self.estado}"


class AsignacionRol(models.Model):

    trabajador_nombre = models.CharField(max_length=100)
    trabajador_apellido = models.CharField(max_length=100)
    trabajador_id = models.PositiveIntegerField()
    rol_nombre = models.CharField(max_length=100)
    rol_id = models.PositiveIntegerField()
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Asignación de Rol"
        verbose_name_plural = "Asignaciones de Roles"
        ordering = ['-fecha_asignacion']

    def clean(self):
        if self.fecha_finalizacion and self.fecha_asignacion:
            if self.fecha_finalizacion < self.fecha_asignacion:
                raise ValidationError('La fecha de finalización no puede ser anterior a la asignación')

    def __str__(self):
        return f"{self.trabajador_nombre} {self.trabajador_apellido} → {self.rol_nombre}"


class AsignacionBus(models.Model):

    trabajador_nombre = models.CharField(max_length=100)
    trabajador_apellido = models.CharField(max_length=100)
    trabajador_id = models.PositiveIntegerField()
    bus_patente = models.CharField(max_length=20)
    bus_modelo = models.CharField(max_length=100)
    bus_id = models.PositiveIntegerField()
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    turno = models.CharField(
        max_length=20,
        choices=[
            ('MAÑANA', 'Mañana'),
            ('TARDE', 'Tarde'),
            ('NOCHE', 'Noche'),
        ],
        default='MAÑANA'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Asignación de Bus"
        verbose_name_plural = "Asignaciones de Buses"
        ordering = ['-fecha_asignacion']

    def clean(self):
        if self.fecha_finalizacion and self.fecha_asignacion:
            if self.fecha_finalizacion < self.fecha_asignacion:
                raise ValidationError('La fecha de finalización no puede ser anterior a la asignación')

    def __str__(self):
        return f"{self.trabajador_nombre} {self.trabajador_apellido} → {self.bus_patente}"