from django.db import models
from django.contrib.auth.models import User


class Tarea(models.Model):
    """
    Modelo para gestionar tareas académicas del usuario.
    Cada tarea pertenece a un usuario y está vinculada a una materia.
    """

    PRIORIDAD_ALTA = 'A'
    PRIORIDAD_MEDIA = 'M'
    PRIORIDAD_BAJA = 'B'
    PRIORIDAD_CHOICES = [
        (PRIORIDAD_ALTA, 'Alta'),
        (PRIORIDAD_MEDIA, 'Media'),
        (PRIORIDAD_BAJA, 'Baja'),
    ]

    ESTADO_PENDIENTE = 'P'
    ESTADO_EN_PROGRESO = 'E'
    ESTADO_TERMINADA = 'T'
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_EN_PROGRESO, 'En progreso'),
        (ESTADO_TERMINADA, 'Terminada'),
    ]

    TIPO_EVIDENCIA = 'V'
    TIPO_TRABAJO = 'W'
    TIPO_EXAMEN = 'X'
    TIPO_ESTUDIO = 'S'
    TIPO_CHOICES = [
        (TIPO_EVIDENCIA, 'Evidencia'),
        (TIPO_TRABAJO, 'Trabajo'),
        (TIPO_EXAMEN, 'Examen'),
        (TIPO_ESTUDIO, 'Estudio'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    materia = models.ForeignKey(
        'materias.Materia',
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    titulo = models.CharField(max_length=255, verbose_name='Título')
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    fecha_limite = models.DateField(verbose_name='Fecha límite')
    prioridad = models.CharField(
        max_length=1,
        choices=PRIORIDAD_CHOICES,
        default=PRIORIDAD_MEDIA,
        verbose_name='Prioridad'
    )
    estado = models.CharField(
        max_length=1,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        verbose_name='Estado'
    )
    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES,
        default=TIPO_EVIDENCIA,
        verbose_name='Tipo'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['fecha_limite', 'prioridad']

    def __str__(self):
        return f'{self.titulo} ({self.get_prioridad_display()})'
