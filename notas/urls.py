from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.listar_notas, name='listar'),
    path('crear/', views.crear_nota, name='crear'),
    path('editar/<int:pk>/', views.editar_nota, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_nota, name='eliminar'),
]

