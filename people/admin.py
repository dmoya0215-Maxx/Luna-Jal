from django.contrib import admin
from .models import People


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'urbanizacion', 'lugar_votacion', 'mesa_votacion', 'activo')
    list_filter = ('activo', 'urbanizacion')
    search_fields = ('nombre', 'apellido', 'telefono', 'correo', 'urbanizacion', 'lugar_votacion', 'mesa_votacion')
    autocomplete_fields = ('referido_por',)
    ordering = ('-activo', 'id')
