
from django import forms
from .models import Trabajador, Rol, Bus, EstadoBus, AsignacionRol, AsignacionBus
from django.core.exceptions import ValidationError
import re
from datetime import date

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'apellido', 'direccion', 'contacto', 'edad', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección completa'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '18',
                'max': '70'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre del Trabajador',
            'apellido': 'Apellido del Trabajador',
            'direccion': 'Dirección',
            'contacto': 'Teléfono de Contacto',
            'edad': 'Edad',
            'activo': '¿Trabajador Activo?'
        }
        help_texts = {
            'contacto': 'Formato: +56 9 1234 5678',
            'edad': 'Debe ser mayor de 18 años',
        }
        error_messages = {
            'nombre': {
                'required': 'El nombre es obligatorio',
                'max_length': 'El nombre no puede exceder 100 caracteres'
            },
            'apellido': {
                'required': 'El apellido es obligatorio',
            },
            'edad': {
                'required': 'La edad es obligatoria',
                'invalid': 'Ingrese una edad válida'
            }
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise ValidationError('El nombre solo puede contener letras')
            if len(nombre) < 2:
                raise ValidationError('El nombre debe tener al menos 2 caracteres')
        return nombre.strip().title()

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido):
                raise ValidationError('El apellido solo puede contener letras')
            if len(apellido) < 2:
                raise ValidationError('El apellido debe tener al menos 2 caracteres')
        return apellido.strip().title()

    def clean_contacto(self):
        contacto = self.cleaned_data.get('contacto')
        if contacto:
           
            contacto_limpio = re.sub(r'[\s\-]', '', contacto)
            if not re.match(r'^\+?[0-9]{8,15}$', contacto_limpio):
                raise ValidationError('Formato de teléfono inválido. Debe contener entre 8 y 15 dígitos')
        return contacto

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad:
            if edad < 18:
                raise ValidationError('El trabajador debe ser mayor de 18 años')
            if edad > 70:
                raise ValidationError('La edad máxima permitida es 70 años')
        return edad

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')
        
        if nombre and apellido:
            if nombre.lower() == apellido.lower():
                raise ValidationError('El nombre y apellido no pueden ser iguales')
        
        return cleaned_data


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'nivel_acceso', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Conductor, Mecánico, Supervisor'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del rol...'
            }),
            'nivel_acceso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre del Rol',
            'descripcion': 'Descripción',
            'nivel_acceso': 'Nivel de Acceso (1-5)',
            'activo': '¿Rol Activo?'
        }
        error_messages = {
            'nombre': {
                'required': 'El nombre del rol es obligatorio',
                'unique': 'Ya existe un rol con este nombre'
            }
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise ValidationError('El nombre del rol solo puede contener letras')
            if len(nombre) < 3:
                raise ValidationError('El nombre debe tener al menos 3 caracteres')
        return nombre.strip().title()

    def clean_nivel_acceso(self):
        nivel = self.cleaned_data.get('nivel_acceso')
        if nivel:
            if nivel < 1 or nivel > 5:
                raise ValidationError('El nivel de acceso debe estar entre 1 y 5')
        return nivel

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) > 500:
            raise ValidationError('La descripción no puede exceder 500 caracteres')
        return descripcion


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['patente', 'modelo', 'año', 'capacidad', 'marca', 'activo']
        widgets = {
            'patente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-123',
                'style': 'text-transform: uppercase;'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Mercedes-Benz O500'
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1990',
                'max': '2025'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '10',
                'max': '80'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Mercedes-Benz, Volvo, Scania'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'patente': 'Patente del Bus',
            'modelo': 'Modelo',
            'año': 'Año de Fabricación',
            'capacidad': 'Capacidad de Pasajeros',
            'marca': 'Marca',
            'activo': '¿Bus Activo?'
        }
        error_messages = {
            'patente': {
                'required': 'La patente es obligatoria',
                'unique': 'Ya existe un bus con esta patente'
            }
        }

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if patente:
            patente = patente.upper().strip()
            if not re.match(r'^[A-Z0-9]{2,4}[-]?[A-Z0-9]{2,4}$', patente):
                raise ValidationError('Formato de patente inválido. Ej: ABC-123 o ABCD-12')
        return patente

    def clean_año(self):
        año = self.cleaned_data.get('año')
        if año:
            año_actual = date.today().year
            if año < 1990:
                raise ValidationError('El año no puede ser anterior a 1990')
            if año > año_actual:
                raise ValidationError(f'El año no puede ser posterior a {año_actual}')
        return año

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad:
            if capacidad < 10:
                raise ValidationError('La capacidad mínima es 10 pasajeros')
            if capacidad > 80:
                raise ValidationError('La capacidad máxima es 80 pasajeros')
        return capacidad

    def clean(self):
        cleaned_data = super().clean()
        año = cleaned_data.get('año')
        capacidad = cleaned_data.get('capacidad')
        
        if año and capacidad:
            if año < 2000 and capacidad > 60:
                raise ValidationError('Buses anteriores al 2000 no suelen tener capacidad mayor a 60 pasajeros')
        
        return cleaned_data


class EstadoBusForm(forms.ModelForm):
    class Meta:
        model = EstadoBus
        fields = ['bus_patente', 'bus_modelo', 'estado', 'observaciones', 'kilometraje']
        widgets = {
            'bus_patente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-123',
                'style': 'text-transform: uppercase;'
            }),
            'bus_modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo del bus'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
            'kilometraje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }
        labels = {
            'bus_patente': 'Patente del Bus',
            'bus_modelo': 'Modelo del Bus',
            'estado': 'Estado Actual',
            'observaciones': 'Observaciones',
            'kilometraje': 'Kilometraje Actual'
        }

    def clean_bus_patente(self):
        patente = self.cleaned_data.get('bus_patente')
        if patente:
            patente = patente.upper().strip()
            if not re.match(r'^[A-Z0-9]{2,4}[-]?[A-Z0-9]{2,4}$', patente):
                raise ValidationError('Formato de patente inválido')
        return patente

    def clean_kilometraje(self):
        kilometraje = self.cleaned_data.get('kilometraje')
        if kilometraje is not None:
            if kilometraje < 0:
                raise ValidationError('El kilometraje no puede ser negativo')
            if kilometraje > 2000000:
                raise ValidationError('El kilometraje parece excesivo. Verifique el valor')
        return kilometraje

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        observaciones = cleaned_data.get('observaciones')
        
        if estado in ['MANTENIMIENTO', 'REPARACION', 'FUERA_SERVICIO']:
            if not observaciones or len(observaciones.strip()) < 10:
                raise ValidationError(
                    f'Para el estado "{estado}" debe proporcionar observaciones detalladas (mínimo 10 caracteres)'
                )
        
        return cleaned_data


class AsignacionRolForm(forms.ModelForm):
    class Meta:
        model = AsignacionRol
        fields = ['trabajador_nombre', 'trabajador_apellido', 'trabajador_id', 
                  'rol_nombre', 'rol_id', 'fecha_finalizacion', 'activo']
        widgets = {
            'trabajador_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'trabajador_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'trabajador_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'rol_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rol_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_finalizacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_trabajador_id(self):
        trabajador_id = self.cleaned_data.get('trabajador_id')
        if trabajador_id:
            if trabajador_id <= 0:
                raise ValidationError('El ID del trabajador debe ser positivo')
            
            if not Trabajador.objects.filter(id=trabajador_id).exists():
                raise ValidationError('No existe un trabajador con este ID')
        return trabajador_id

    def clean_rol_id(self):
        rol_id = self.cleaned_data.get('rol_id')
        if rol_id:
            if rol_id <= 0:
                raise ValidationError('El ID del rol debe ser positivo')
            
            if not Rol.objects.filter(id=rol_id).exists():
                raise ValidationError('No existe un rol con este ID')
        return rol_id

    def clean_fecha_finalizacion(self):
        fecha_fin = self.cleaned_data.get('fecha_finalizacion')
        if fecha_fin:
            if fecha_fin < date.today():
                raise ValidationError('La fecha de finalización no puede ser en el pasado')
        return fecha_fin


class AsignacionBusForm(forms.ModelForm):
    class Meta:
        model = AsignacionBus
        fields = ['trabajador_nombre', 'trabajador_apellido', 'trabajador_id',
                  'bus_patente', 'bus_modelo', 'bus_id', 'fecha_finalizacion', 
                  'turno', 'activo']
        widgets = {
            'trabajador_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'trabajador_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'trabajador_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'bus_patente': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform: uppercase;'
            }),
            'bus_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'bus_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_finalizacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_trabajador_id(self):
        trabajador_id = self.cleaned_data.get('trabajador_id')
        if trabajador_id:
            if trabajador_id <= 0:
                raise ValidationError('El ID del trabajador debe ser positivo')
            if not Trabajador.objects.filter(id=trabajador_id).exists():
                raise ValidationError('No existe un trabajador con este ID')
        return trabajador_id

    def clean_bus_id(self):
        bus_id = self.cleaned_data.get('bus_id')
        if bus_id:
            if bus_id <= 0:
                raise ValidationError('El ID del bus debe ser positivo')
            if not Bus.objects.filter(id=bus_id).exists():
                raise ValidationError('No existe un bus con este ID')
        return bus_id

    def clean(self):
        cleaned_data = super().clean()
        trabajador_id = cleaned_data.get('trabajador_id')
        bus_id = cleaned_data.get('bus_id')
        turno = cleaned_data.get('turno')
        activo = cleaned_data.get('activo')
        
        if trabajador_id and bus_id and activo:
            existe = AsignacionBus.objects.filter(
                trabajador_id=trabajador_id,
                bus_id=bus_id,
                activo=True
            )

            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            
            if existe.exists():
                raise ValidationError('Ya existe una asignación activa para este trabajador y bus')
        
        return cleaned_data