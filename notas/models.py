from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Nota(models.Model):
    """
    Modelo para almacenar notas de usuario.
    Cada nota pertenece a un usuario y es privada.
    Puede estar relacionada opcionalmente con una materia.

    Nota:
    - El campo «contenido» almacena HTML generado por el editor enriquecido (QuillJS).
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notas')
    materia = models.ForeignKey(
        'materias.Materia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notas',
        verbose_name='Materia'
    )
    titulo = models.CharField(max_length=255, verbose_name='Título')
    # Guarda el contenido HTML producido por el editor (rich text)
    contenido = models.TextField(verbose_name='Contenido (HTML)')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-fecha_creacion']  # Más recientes primero

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
