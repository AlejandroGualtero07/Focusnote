from django.contrib import admin
from .models import Nota


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Nota"""
    list_display = ('titulo', 'usuario', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('fecha_creacion', 'usuario')
    search_fields = ('titulo', 'contenido', 'usuario__username')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    date_hierarchy = 'fecha_creacion'
