from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.listar_tareas, name='listar'),
    path('crear/', views.crear_tarea, name='crear'),
    path('editar/<int:pk>/', views.editar_tarea, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_tarea, name='eliminar'),
]



