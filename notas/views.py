from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Nota
from materias.models import Materia

try:
    import bleach
except ImportError:  # pragma: no cover - dependencia opcional
    bleach = None


ALLOWED_NOTE_TAGS = [
    'p', 'br', 'strong', 'b', 'em', 'i', 'u',
    'ul', 'ol', 'li',
    'h1', 'h2', 'h3',
    'blockquote', 'code', 'pre',
]
ALLOWED_NOTE_ATTRS = {
    '*': ['class'],
}


def sanitize_html(contenido: str) -> str:
    """
    Sanitiza el HTML generado por el editor (QuillJS) para prevenir XSS.
    Si bleach no está disponible, devuelve el contenido tal cual.
    """
    if not contenido:
        return ''
    if bleach is None:
        # En producción se recomienda instalar bleach.
        return contenido
    return bleach.clean(
        contenido,
        tags=ALLOWED_NOTE_TAGS,
        attributes=ALLOWED_NOTE_ATTRS,
        strip=True,
    )


@login_required
def listar_notas(request):
    """
    Lista todas las notas del usuario autenticado.
    Solo muestra las notas que pertenecen al usuario actual.
    """
    notas = Nota.objects.filter(usuario=request.user)
    return render(request, 'notas/lista.html', {'notas': notas})


@login_required
def crear_nota(request):
    """
    Crea una nueva nota para el usuario autenticado.
    Permite asignar una materia opcional.
    """
    materias = Materia.objects.filter(usuario=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        contenido_raw = request.POST.get('contenido', '').strip()
        materia_id = request.POST.get('materia', '')

        if not titulo:
            messages.error(request, 'El título es obligatorio.')
        else:
            materia = None
            if materia_id:
                try:
                    materia = Materia.objects.get(pk=materia_id, usuario=request.user)
                except Materia.DoesNotExist:
                    messages.warning(request, 'La materia seleccionada no existe.')

            contenido = sanitize_html(contenido_raw)

            Nota.objects.create(
                usuario=request.user,
                titulo=titulo,
                contenido=contenido,
                materia=materia
            )
            messages.success(request, 'Nota creada exitosamente.')
            return redirect('notas:listar')

    context = {
        'materias': materias,
        'nota': None,
        'modo': 'crear',
    }
    return render(request, 'notas/editor.html', context)


@login_required
def editar_nota(request, pk):
    """
    Edita una nota existente.
    Solo permite editar notas que pertenecen al usuario autenticado.
    Permite cambiar la materia asignada.
    """
    nota = get_object_or_404(Nota, pk=pk, usuario=request.user)
    materias = Materia.objects.filter(usuario=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        contenido_raw = request.POST.get('contenido', '').strip()
        materia_id = request.POST.get('materia', '')

        if not titulo:
            messages.error(request, 'El título es obligatorio.')
        else:
            materia = None
            if materia_id:
                try:
                    materia = Materia.objects.get(pk=materia_id, usuario=request.user)
                except Materia.DoesNotExist:
                    messages.warning(request, 'La materia seleccionada no existe.')

            contenido = sanitize_html(contenido_raw)

            nota.titulo = titulo
            nota.contenido = contenido
            nota.materia = materia
            nota.save()
            messages.success(request, 'Nota actualizada exitosamente.')
            return redirect('notas:listar')

    context = {
        'nota': nota,
        'materias': materias,
        'modo': 'editar',
    }
    return render(request, 'notas/editor.html', context)


@login_required
def eliminar_nota(request, pk):
    """
    Elimina una nota.
    Solo permite eliminar notas que pertenecen al usuario autenticado.
    """
    nota = get_object_or_404(Nota, pk=pk, usuario=request.user)

    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada exitosamente.')
        return redirect('notas:listar')

    return render(request, 'notas/eliminar.html', {'nota': nota})
