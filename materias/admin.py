from django.contrib import admin
from .models import Materia


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Materia"""
    list_display = ('nombre', 'usuario', 'color', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'color', 'usuario')
    search_fields = ('nombre', 'descripcion', 'usuario__username')
    readonly_fields = ('fecha_creacion',)
    date_hierarchy = 'fecha_creacion'
