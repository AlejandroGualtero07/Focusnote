from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materias', '0001_initial'),
        ('tareas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PomodoroSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion_minutos', models.PositiveIntegerField(verbose_name='Duración (minutos)')),
                ('tipo_sesion', models.CharField(choices=[('E', 'Estudio'), ('D', 'Descanso')], default='E', max_length=1, verbose_name='Tipo de sesión')),
                ('fecha_inicio', models.DateTimeField(verbose_name='Fecha de inicio')),
                ('completada', models.BooleanField(default=False, verbose_name='Completada')),
                ('materia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pomodoro_sessions', to='materias.materia')),
                ('tarea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pomodoro_sessions', to='tareas.tarea')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pomodoro_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sesión Pomodoro',
                'verbose_name_plural': 'Sesiones Pomodoro',
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]




