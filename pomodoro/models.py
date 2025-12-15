from django.db import models
from django.contrib.auth.models import User


class PomodoroSession(models.Model):
    """
    Registro de una sesión Pomodoro (estudio o descanso).
    Se utiliza para alimentar el módulo de progreso.
    """

    TIPO_ESTUDIO = 'E'
    TIPO_DESCANSO = 'D'
    TIPO_CHOICES = [
        (TIPO_ESTUDIO, 'Estudio'),
        (TIPO_DESCANSO, 'Descanso'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pomodoro_sessions'
    )
    materia = models.ForeignKey(
        'materias.Materia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pomodoro_sessions'
    )
    tarea = models.ForeignKey(
        'tareas.Tarea',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pomodoro_sessions'
    )
    duracion_minutos = models.PositiveIntegerField(
        verbose_name='Duración (minutos)'
    )
    tipo_sesion = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES,
        default=TIPO_ESTUDIO,
        verbose_name='Tipo de sesión'
    )
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha de inicio'
    )
    completada = models.BooleanField(
        default=False,
        verbose_name='Completada'
    )

    class Meta:
        verbose_name = 'Sesión Pomodoro'
        verbose_name_plural = 'Sesiones Pomodoro'
        ordering = ['-fecha_inicio']

    def __str__(self):
        tipo = self.get_tipo_sesion_display()
        return f'{tipo} - {self.duracion_minutos} min - {self.usuario.username}'
