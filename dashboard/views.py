from django.shortcuts import render
from user.decorators import login_required_custom
from user.models import User
from people.models import People

@login_required_custom
def dashboard_view(request):
    """Vista del dashboard principal con estadísticas dinámicas"""
    # Obtener estadísticas de la base de datos
    total_usuarios = User.objects.count()
    total_personas = People.objects.count()
    total_urbanizaciones = People.objects.count()
    total_referidos = People.objects.filter(referido_por__isnull=False).count()
    usuarios_activos = User.objects.filter(cargo="Admin").count()
    
    context = {
        'page_title': 'Panel de Control',
        'page_subtitle': 'Bienvenido al sistema Luna',
        'total_usuarios': total_usuarios,
        'total_personas': total_personas,
        'total_urbanizaciones': total_urbanizaciones,
        'total_referidos': total_referidos,
        'usuarios_activos': usuarios_activos,
    }
    return render(request, 'dashboard/dashboard.html', context)

