from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', include('accounts.urls')),
    path('notas/', include('notas.urls')),
    path('materias/', include('materias.urls')),
    path('tareas/', include('tareas.urls')),
    path('pomodoro/', include('pomodoro.urls')),
    path('progreso/', include('progreso.urls')),
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
