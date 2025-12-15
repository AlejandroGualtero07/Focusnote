from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """
    Modelo de perfil de usuario con relación OneToOne a User.
    Almacena información adicional del usuario como foto de perfil e información relevante.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario'
    )
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    informacion_relevante = models.TextField(
        blank=True,
        null=True,
        verbose_name='Información relevante',
        help_text='Información adicional sobre ti (opcional)'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
