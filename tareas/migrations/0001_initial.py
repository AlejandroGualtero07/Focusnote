from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha_limite', models.DateField(verbose_name='Fecha límite')),
                ('prioridad', models.CharField(choices=[('A', 'Alta'), ('M', 'Media'), ('B', 'Baja')], default='M', max_length=1, verbose_name='Prioridad')),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('E', 'En progreso'), ('T', 'Terminada')], default='P', max_length=1, verbose_name='Estado')),
                ('tipo', models.CharField(choices=[('V', 'Evidencia'), ('W', 'Trabajo'), ('X', 'Examen'), ('S', 'Estudio')], default='V', max_length=1, verbose_name='Tipo')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to='materias.materia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tarea',
                'verbose_name_plural': 'Tareas',
                'ordering': ['fecha_limite', 'prioridad'],
            },
        ),
    ]




