from django.db import models
from django.contrib.auth.models import User


class Materia(models.Model):
    """
    Modelo para almacenar materias de usuario.
    Cada materia pertenece a un usuario y puede tener un color personalizado.
    """
    COLORES_CHOICES = [
        ('primary', 'Azul'),
        ('success', 'Verde'),
        ('danger', 'Rojo'),
        ('warning', 'Amarillo'),
        ('info', 'Cian'),
        ('secondary', 'Gris'),
        ('dark', 'Negro'),
        ('purple', 'Morado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='materias')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    color = models.CharField(
        max_length=20,
        choices=COLORES_CHOICES,
        default='primary',
        verbose_name='Color'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['nombre']  # Orden alfabético

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
