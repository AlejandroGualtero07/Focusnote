from django.urls import path
from . import views

app_name = 'pomodoro'

urlpatterns = [
    path('', views.pomodoro_view, name='inicio'),
    path('registrar/', views.registrar_sesion, name='registrar_sesion'),
]

