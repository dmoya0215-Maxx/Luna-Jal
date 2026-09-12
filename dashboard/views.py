from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.db.models import Q
from user.decorators import login_required_custom
from user.models import User
from people.models import People

@login_required_custom
@never_cache
def dashboard_view(request):
    """Vista del dashboard principal con estadísticas dinámicas y en tiempo real"""
    
    # 1. Total de Usuarios
    total_usuarios = User.objects.count()

    # 2. Total de Personas
    total_personas = People.objects.count()

    # 3. Total de Urbanizaciones distintas registradas en la tabla People
    # Excluye valores nulos, vacíos y espacios en blanco
    total_urbanizaciones = People.objects.exclude(
        Q(urbanizacion__isnull=True) | Q(urbanizacion__exact="") | Q(urbanizacion__exact=" ")
    ).values('urbanizacion').distinct().count()

    # 4. Total de Personas Referidas (Registros que tienen asignado un referido_por)
    total_referidos = People.objects.filter(referido_por__isnull=False).count()

    # 5. Total de Administradores
    total_admins = User.objects.filter(cargo="Admin").count()

    context = {
        'page_title': 'Panel de Control',
        'page_subtitle': 'Bienvenido al sistema Luna',
        'total_users': total_usuarios,
        'total_personas': total_personas,
        'total_urbanizaciones': total_urbanizaciones,
        'total_referidos': total_referidos,
        'total_admins': total_admins,
    }
    
    return render(request, 'dashboard/dashboard.html', context)