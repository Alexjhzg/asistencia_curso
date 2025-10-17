# asistencia/models.py
from django.db import models
from django.core.exceptions import ValidationError

class Sexo(models.Model):
    # id es autoincremental por defecto (equivale a INT AUTO_INCREMENT PRIMARY KEY)
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

class NivelEducativo(models.Model):
    # id es autoincremental por defecto
    nombre = models.CharField(max_length=50) # Aumentar si los textos reales son muy largos

    def __str__(self):
        return self.nombre

class Organizacion(models.Model):
    # id es autoincremental por defecto
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Estado(models.Model): # Estados geográficos
    # id es autoincremental por defecto
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

class Coordinacion(models.Model):
    # id es autoincremental por defecto
    # Aumentar max_length para manejar nombres largos
    nombre = models.CharField(max_length=100) # Cambiado de 50 a 100

    def __str__(self):
        return self.nombre

class Alianza(models.Model):
    # id es autoincremental por defecto
    nombre = models.TextField() # TextField puede manejar textos largos si es necesario

    def __str__(self):
        return self.nombre

class Gerencia(models.Model):
    # id es autoincremental por defecto
    # Aumentar max_length si los nombres del Excel son muy largos
    nombre = models.CharField(max_length=100) # Cambiado de 50 a 100
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.organizacion.nombre})"

class CargoSegen(models.Model):
    # id es autoincremental por defecto
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    # id es autoincremental por defecto
    # Aumentar max_length si los nombres del Excel/XLSForm son muy largos
    nombre = models.CharField(max_length=100) # Cambiado de 50 a 100
    gerencia_contexto = models.ForeignKey(Gerencia, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.gerencia_contexto.nombre if self.gerencia_contexto else 'Sin Gerencia'})"

class Ubicacion(models.Model):
    # id es autoincremental por defecto
    nombre = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    # id es autoincremental por defecto
    tema = models.CharField(max_length=255)
    fecha_curso = models.DateField()

    def __str__(self):
        return f"{self.tema} - {self.fecha_curso.strftime('%d/%m/%Y')}"

class Persona(models.Model):
    cedula = models.CharField(max_length=8, primary_key=True) # Este SI debe ser la PK
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    edad = models.IntegerField(null=True, blank=True) # Permitir nulos si no se conoce
    profesion = models.CharField(max_length=100, blank=True, null=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE) # FK a la tabla Sexo
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE) # FK a la tabla NivelEducativo

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cedula})"

    # Validación personalizada (opcional, se puede hacer en el formulario también)
    def clean(self):
        if self.edad is not None and (self.edad <= 0 or self.edad >= 100):
            raise ValidationError('La edad debe estar entre 1 y 99.')

class PerfilLaboral(models.Model):
    cedula = models.OneToOneField(Persona, on_delete=models.CASCADE, primary_key=True) # PK es la FK a Persona
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
    coordinacion = models.ForeignKey(Coordinacion, on_delete=models.SET_NULL, null=True, blank=True)
    cargo_segen = models.ForeignKey(CargoSegen, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE) # Asumiendo que siempre tiene gerencia
    alianza = models.ForeignKey(Alianza, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.cedula.nombre} {self.cedula.apellido}"

class ParticipacionCurso(models.Model):
    cedula = models.ForeignKey(Persona, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=11, blank=True, null=True) # Permitir nulos
    otro_telefono = models.CharField(max_length=11, blank=True, null=True) # Permitir nulos
    comentario = models.TextField(blank=True, null=True) # Permitir nulos
    hora_registro = models.DateTimeField(auto_now_add=True) # Se asigna automáticamente
    registrado = models.BooleanField() # TINYINT(1) en MySQL
    encuentra = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cedula', 'curso_id') # Clave primaria compuesta

    def __str__(self):
        return f"Participación de {self.cedula.nombre} {self.cedula.apellido} en {self.curso_id.tema}"

    # Validación personalizada para teléfonos (opcional, se puede hacer en el formulario también)
    def clean(self):
        import re
        if self.telefono and not re.match(r'^\d{11}$', self.telefono):
            raise ValidationError({'telefono': 'El número de teléfono debe tener 11 dígitos numéricos.'})
        if self.otro_telefono and not re.match(r'^\d{11}$', self.otro_telefono):
            raise ValidationError({'otro_telefono': 'El número de otro teléfono debe tener 11 dígitos numéricos.'})
