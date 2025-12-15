from .models import Perfil


def perfil_context(request):
    """
    Context processor para asegurar que el perfil esté disponible en todos los templates.
    Crea automáticamente un perfil si no existe.
    """
    if request.user.is_authenticated:
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        return {'user_perfil': perfil}
    return {'user_perfil': None}


