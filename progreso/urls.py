from django.urls import path
from . import views

app_name = 'progreso'

urlpatterns = [
    path('', views.dashboard_progreso, name='dashboard'),
]

