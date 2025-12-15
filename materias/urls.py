from django.urls import path
from . import views

app_name = 'materias'

urlpatterns = [
    path('', views.listar_materias, name='listar'),
    path('crear/', views.crear_materia, name='crear'),
    path('editar/<int:pk>/', views.editar_materia, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_materia, name='eliminar'),
    path('<int:pk>/', views.detalle_materia, name='detalle'),
]

