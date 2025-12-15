from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render

from materias.models import Materia
from tareas.models import Tarea
from pomodoro.models import PomodoroSession


@login_required
def dashboard_progreso(request):
    """
    Dashboard de progreso del usuario.
    Solo lectura: consolida estadísticas de Tareas y sesiones Pomodoro.
    """
    user = request.user

    # --- Progreso de tareas ---
    tareas_qs = Tarea.objects.filter(usuario=user)
    total_tareas = tareas_qs.count()
    tareas_pendientes = tareas_qs.filter(estado='P').count()
    tareas_en_progreso = tareas_qs.filter(estado='E').count()
    tareas_terminadas = tareas_qs.filter(estado='T').count()

    tareas_chart = {
        'labels': ['Pendientes', 'En progreso', 'Terminadas'],
        'data': [tareas_pendientes, tareas_en_progreso, tareas_terminadas],
    }

    # --- Tiempo de estudio (Pomodoro) ---
    sesiones_estudio = PomodoroSession.objects.filter(
        usuario=user,
        tipo_sesion=PomodoroSession.TIPO_ESTUDIO,
    )

    total_estudio_minutos = sesiones_estudio.aggregate(
        total=Sum('duracion_minutos')
    )['total'] or 0

    sesiones_estudio_completadas = sesiones_estudio.filter(
        completada=True
    ).count()

    # Desglose de estudio por materia
    estudio_por_materia_qs = sesiones_estudio.exclude(materia__isnull=True).values(
        'materia__nombre',
        'materia__color',
    ).annotate(
        minutos=Sum('duracion_minutos')
    ).order_by('-minutos')

    estudio_materias_labels = [item['materia__nombre'] for item in estudio_por_materia_qs]
    estudio_materias_data = [item['minutos'] for item in estudio_por_materia_qs]

    context = {
        # KPIs Tareas
        'total_tareas': total_tareas,
        'tareas_pendientes': tareas_pendientes,
        'tareas_en_progreso': tareas_en_progreso,
        'tareas_terminadas': tareas_terminadas,
        'tareas_chart': tareas_chart,
        # KPIs Pomodoro
        'total_estudio_minutos': total_estudio_minutos,
        'sesiones_estudio_completadas': sesiones_estudio_completadas,
        'estudio_materias_labels': estudio_materias_labels,
        'estudio_materias_data': estudio_materias_data,
    }

    return render(request, 'progreso/dashboard.html', context)
