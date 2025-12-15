from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil
from .forms import PerfilForm


@login_required
def perfil_view(request):
    """
    Vista para ver y editar el perfil del usuario.
    Crea automáticamente un perfil si no existe.
    """
    # Obtener o crear el perfil del usuario
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil:ver')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = PerfilForm(instance=perfil)
    
    context = {
        'perfil': perfil,
        'form': form,
    }
    return render(request, 'accounts/perfil.html', context)
