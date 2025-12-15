from datetime import datetime, timezone as dt_timezone

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from materias.models import Materia
from tareas.models import Tarea
from .models import PomodoroSession


@login_required
def pomodoro_view(request):
    """
    Vista del temporizador Pomodoro.
    Permite asociar la sesión a una materia y, opcionalmente, a una tarea.
    """
    materias = Materia.objects.filter(usuario=request.user).order_by('nombre')
    tareas = Tarea.objects.filter(usuario=request.user).order_by('fecha_limite')

    contexto = {
        'materias': materias,
        'tareas': tareas,
    }
    return render(request, 'pomodoro/timer.html', contexto)


@login_required
@require_POST
def registrar_sesion(request):
    """
    Endpoint AJAX para registrar una sesión Pomodoro.
    Espera:
    - tipo_sesion: 'E' (estudio) o 'D' (descanso)
    - duracion_segundos: duración efectiva en segundos
    - materia_id (opcional)
    - tarea_id (opcional)
    - completada: 'true' / 'false'
    - fecha_inicio_iso: fecha/hora de inicio en ISO (opcional; si no, ahora)
    """
    try:
        tipo_sesion = request.POST.get('tipo_sesion', 'E')
        duracion_segundos = int(request.POST.get('duracion_segundos', '0'))
        materia_id = request.POST.get('materia_id') or None
        tarea_id = request.POST.get('tarea_id') or None
        completada_str = request.POST.get('completada', 'false')
        fecha_inicio_iso = request.POST.get('fecha_inicio_iso')
    except (TypeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Datos inválidos.'}, status=400)

    if tipo_sesion not in dict(PomodoroSession.TIPO_CHOICES):
        return JsonResponse({'ok': False, 'error': 'Tipo de sesión inválido.'}, status=400)

    # Convertir duración a minutos, con un mínimo de 1 minuto útil
    duracion_minutos = max(1, round(duracion_segundos / 60)) if duracion_segundos > 0 else 0
    if duracion_minutos <= 0:
        return JsonResponse({'ok': False, 'error': 'Duración insuficiente.'}, status=400)

    # Parsear fecha de inicio (si se envía); si no, usar ahora (UTC)
    if fecha_inicio_iso:
        try:
            fecha_inicio = datetime.fromisoformat(fecha_inicio_iso)
            if fecha_inicio.tzinfo is None:
                fecha_inicio = fecha_inicio.replace(tzinfo=dt_timezone.utc)
        except ValueError:
            fecha_inicio = datetime.now(dt_timezone.utc)
    else:
        fecha_inicio = datetime.now(dt_timezone.utc)

    materia = None
    tarea = None

    if materia_id:
        try:
            materia = Materia.objects.get(pk=materia_id, usuario=request.user)
        except Materia.DoesNotExist:
            materia = None

    if tarea_id:
        try:
            tarea = Tarea.objects.get(pk=tarea_id, usuario=request.user)
        except Tarea.DoesNotExist:
            tarea = None

    completada = completada_str.lower() == 'true'

    PomodoroSession.objects.create(
        usuario=request.user,
        materia=materia,
        tarea=tarea,
        duracion_minutos=duracion_minutos,
        tipo_sesion=tipo_sesion,
        fecha_inicio=fecha_inicio,
        completada=completada,
    )

    return JsonResponse({'ok': True})
