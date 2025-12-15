from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import date
from notas.models import Nota
from materias.models import Materia
from tareas.models import Tarea
from pomodoro.models import PomodoroSession


@login_required
def home(request):
    """Dashboard principal - datos básicos del usuario."""
    usuario = request.user
    hoy = date.today()

    total_notas = Nota.objects.filter(usuario=usuario).count()
    total_materias = Materia.objects.filter(usuario=usuario).count()
    
    # Tareas pendientes (estado 'P')
    total_tareas = Tarea.objects.filter(usuario=usuario, estado='P').count()
    
    # Tareas de hoy: fecha_limite = hoy y estado = 'P' (Pendiente)
    tareas_hoy = Tarea.objects.filter(
        usuario=usuario,
        fecha_limite=hoy,
        estado='P'
    ).order_by('prioridad', 'fecha_limite')[:5]
    
    # Calcular tiempo enfocado hoy (sesiones Pomodoro completadas hoy)
    sesiones_hoy = PomodoroSession.objects.filter(
        usuario=usuario,
        tipo_sesion=PomodoroSession.TIPO_ESTUDIO,
        completada=True,
        fecha_inicio__date=hoy
    )
    tiempo_enfocado_minutos = sesiones_hoy.aggregate(
        total=Sum('duracion_minutos')
    )['total'] or 0
    
    # Formatear tiempo enfocado
    horas = tiempo_enfocado_minutos // 60
    minutos = tiempo_enfocado_minutos % 60
    tiempo_enfocado_hoy = f"{horas}h {minutos:02d}m"

    ultimas_notas = Nota.objects.filter(usuario=usuario).order_by("-fecha_creacion")[:5]

    context = {
        "total_notas": total_notas,
        "total_materias": total_materias,
        "total_tareas": total_tareas,
        "tiempo_enfocado_hoy": tiempo_enfocado_hoy,
        "ultimas_notas": ultimas_notas,
        "tareas_hoy": tareas_hoy,
    }
    return render(request, "dashboard.html", context)


def login_view(request):
    """
    Vista de login funcional
    - Autentica usuario con username y password
    - Muestra mensaje de error si las credenciales son incorrectas
    - Redirige al home si el login es exitoso
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect("/")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "accounts/login.html")


def register_view(request):
    """
    Vista de registro de usuario
    - Valida que el usuario no exista
    - Crea nuevo usuario con User.objects.create_user
    - Redirige al login después del registro exitoso
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validar que el usuario no exista
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe. Por favor, elige otro.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
        elif not username or not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
        else:
            # Crear nuevo usuario
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, "¡Cuenta creada exitosamente! Por favor, inicia sesión.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Error al crear la cuenta: {str(e)}")

    return render(request, "accounts/register.html")


def logout_view(request):
    """
    Vista de logout
    - Cierra la sesión del usuario
    - Redirige al login
    """
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")
