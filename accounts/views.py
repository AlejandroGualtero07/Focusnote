from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Perfil

@login_required
def perfil_view(request):
    """
    Vista para mostrar y gestionar el perfil del usuario.
    """
    # Obtener o crear el perfil del usuario de manera segura
    perfil, created = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'informacion_relevante': ''}
    )
    
    context = {
        'perfil': perfil,
    }
    return render(request, "accounts/perfil.html", context)

def home(request):
    return render(request, "layout/home.html")
