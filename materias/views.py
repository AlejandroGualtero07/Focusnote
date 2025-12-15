from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Materia


@login_required
def listar_materias(request):
    """
    Lista todas las materias del usuario autenticado.
    Solo muestra las materias que pertenecen al usuario actual.
    """
    materias = Materia.objects.filter(usuario=request.user)
    return render(request, 'materias/listar.html', {'materias': materias})


@login_required
def crear_materia(request):
    """
    Crea una nueva materia para el usuario autenticado.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        color = request.POST.get('color', 'primary')

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            # Verificar que no exista una materia con el mismo nombre para este usuario
            if Materia.objects.filter(usuario=request.user, nombre=nombre).exists():
                messages.error(request, 'Ya tienes una materia con ese nombre.')
            else:
                materia = Materia.objects.create(
                    usuario=request.user,
                    nombre=nombre,
                    descripcion=descripcion if descripcion else None,
                    color=color
                )
                messages.success(request, 'Materia creada exitosamente.')
                return redirect('materias:listar')

    return render(request, 'materias/crear.html')


@login_required
def editar_materia(request, pk):
    """
    Edita una materia existente.
    Solo permite editar materias que pertenecen al usuario autenticado.
    """
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        color = request.POST.get('color', 'primary')

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            # Verificar que no exista otra materia con el mismo nombre (excluyendo la actual)
            if Materia.objects.filter(usuario=request.user, nombre=nombre).exclude(pk=pk).exists():
                messages.error(request, 'Ya tienes una materia con ese nombre.')
            else:
                materia.nombre = nombre
                materia.descripcion = descripcion if descripcion else None
                materia.color = color
                materia.save()
                messages.success(request, 'Materia actualizada exitosamente.')
                return redirect('materias:listar')

    return render(request, 'materias/editar.html', {'materia': materia})


@login_required
def eliminar_materia(request, pk):
    """
    Elimina una materia.
    Solo permite eliminar materias que pertenecen al usuario autenticado.
    """
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)

    if request.method == 'POST':
        nombre_materia = materia.nombre
        materia.delete()
        messages.success(request, f'Materia "{nombre_materia}" eliminada exitosamente.')
        return redirect('materias:listar')

    return render(request, 'materias/eliminar.html', {'materia': materia})


@login_required
def detalle_materia(request, pk):
    """
    Muestra el detalle de una materia con sus notas asociadas.
    """
    materia = get_object_or_404(Materia, pk=pk, usuario=request.user)
    notas = materia.notas.all()
    return render(request, 'materias/detalle.html', {
        'materia': materia,
        'notas': notas
    })
