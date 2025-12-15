from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from materias.models import Materia
from .models import Tarea


@login_required
def listar_tareas(request):
    """
    Lista las tareas del usuario autenticado, con posibilidad de filtrar por estado.
    """
    estado = request.GET.get('estado', '').upper()

    tareas = Tarea.objects.filter(usuario=request.user).select_related('materia')
    if estado in {c[0] for c in Tarea.ESTADO_CHOICES}:
        tareas = tareas.filter(estado=estado)

    contexto = {
        'tareas': tareas,
        'estado_actual': estado,
    }
    return render(request, 'tareas/lista.html', contexto)


@login_required
def crear_tarea(request):
    """
    Crea una nueva tarea para el usuario autenticado.
    """
    materias = Materia.objects.filter(usuario=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        materia_id = request.POST.get('materia', '')
        fecha_limite_str = request.POST.get('fecha_limite', '').strip()
        prioridad = request.POST.get('prioridad', Tarea.PRIORIDAD_MEDIA)
        tipo = request.POST.get('tipo', Tarea.TIPO_EVIDENCIA)

        if not titulo:
            messages.error(request, 'El título es obligatorio.')
        else:
            # Validar materia
            try:
                materia = Materia.objects.get(pk=materia_id, usuario=request.user)
            except (Materia.DoesNotExist, ValueError, TypeError):
                messages.error(request, 'La materia seleccionada no es válida.')
                materia = None

            # Validar fecha
            try:
                year, month, day = map(int, fecha_limite_str.split('-'))
                fecha_limite = date(year, month, day)
            except Exception:
                messages.error(request, 'La fecha límite no es válida.')
                fecha_limite = None

            if materia and fecha_limite:
                Tarea.objects.create(
                    usuario=request.user,
                    materia=materia,
                    titulo=titulo,
                    descripcion=descripcion or None,
                    fecha_limite=fecha_limite,
                    prioridad=prioridad,
                    tipo=tipo,
                    # Estado por defecto: pendiente
                )
                messages.success(request, 'Tarea creada correctamente.')
                return redirect('tareas:listar')

    contexto = {
        'materias': materias,
        'modo': 'crear',
    }
    return render(request, 'tareas/crear.html', contexto)


@login_required
def editar_tarea(request, pk):
    """
    Edita una tarea existente (solo del usuario actual).
    Permite cambiar estado, fecha límite, prioridad y tipo.
    """
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    materias = Materia.objects.filter(usuario=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        materia_id = request.POST.get('materia', '')
        fecha_limite_str = request.POST.get('fecha_limite', '').strip()
        prioridad = request.POST.get('prioridad', tarea.prioridad)
        tipo = request.POST.get('tipo', tarea.tipo)
        estado = request.POST.get('estado', tarea.estado)

        if not titulo:
            messages.error(request, 'El título es obligatorio.')
        else:
            try:
                materia = Materia.objects.get(pk=materia_id, usuario=request.user)
            except (Materia.DoesNotExist, ValueError, TypeError):
                messages.error(request, 'La materia seleccionada no es válida.')
                materia = None

            try:
                year, month, day = map(int, fecha_limite_str.split('-'))
                fecha_limite = date(year, month, day)
            except Exception:
                messages.error(request, 'La fecha límite no es válida.')
                fecha_limite = None

            if materia and fecha_limite:
                tarea.titulo = titulo
                tarea.descripcion = descripcion or None
                tarea.materia = materia
                tarea.fecha_limite = fecha_limite
                tarea.prioridad = prioridad
                tarea.tipo = tipo
                tarea.estado = estado
                tarea.save()

                messages.success(request, 'Tarea actualizada correctamente.')
                return redirect('tareas:listar')

    contexto = {
        'tarea': tarea,
        'materias': materias,
        'modo': 'editar',
    }
    return render(request, 'tareas/crear.html', contexto)


@login_required
def eliminar_tarea(request, pk):
    """
    Elimina una tarea del usuario autenticado.
    """
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)

    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada correctamente.')
        return redirect('tareas:listar')

    return render(request, 'tareas/eliminar.html', {'tarea': tarea})
