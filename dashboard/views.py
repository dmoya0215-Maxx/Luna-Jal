from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.db.models import Count, Q
from user.decorators import login_required_custom
from user.models import User
from people.models import People, VEREDA_PREFIX

@login_required_custom
@never_cache
def dashboard_view(request):
    """Vista del dashboard principal con estadísticas dinámicas y en tiempo real"""

    # Filtros del reporte de personas por urbanización o vereda
    tipo = request.GET.get('tipo', '').strip()
    buscar = request.GET.get('buscar', '').strip()

    # 1. Total de Usuarios
    total_usuarios = User.objects.count()

    # 2. Total de Personas
    total_personas = People.objects.count()

    # 3. Total de Urbanizaciones distintas registradas en la tabla People
    # Excluye valores nulos, vacíos y espacios en blanco
    base = People.objects.exclude(
        Q(urbanizacion__isnull=True) | Q(urbanizacion__exact="") | Q(urbanizacion__exact=" ")
    )
    total_urbanizaciones = base.values('urbanizacion').distinct().count()

    # 4. Total de Personas Referidas (Registros que tienen asignado un referido_por)
    total_referidos = People.objects.filter(referido_por__isnull=False).count()

    # 5. Total de Administradores
    total_admins = User.objects.filter(cargo="Admin").count()

    # 6. Personas activas e inactivas (global, sin filtros)
    total_activas = People.objects.filter(activo=True).count()
    total_inactivas = People.objects.filter(activo=False).count()

    # 7. Activas e inactivas agrupadas por urbanización o vereda
    if tipo == 'vereda':
        base = base.filter(urbanizacion__startswith=VEREDA_PREFIX)
    elif tipo == 'urbanizacion':
        base = base.exclude(urbanizacion__startswith=VEREDA_PREFIX)

    if buscar:
        base = base.filter(urbanizacion__icontains=buscar)

    resumen = (
        base
        .values('urbanizacion')
        .annotate(
            activas=Count('id', filter=Q(activo=True)),
            inactivas=Count('id', filter=Q(activo=False)),
        )
        .order_by('urbanizacion')
    )

    filas = []
    for item in resumen:
        subtotal = item['activas'] + item['inactivas']
        filas.append({
            'nombre': item['urbanizacion'],
            'es_vereda': item['urbanizacion'].startswith(VEREDA_PREFIX),
            'activas': item['activas'],
            'inactivas': item['inactivas'],
            'total': subtotal,
            'porcentaje_activas': round(item['activas'] * 100 / subtotal) if subtotal else 0,
        })

    filas.sort(key=lambda fila: (-fila['total'], fila['nombre']))

    # 8. Totales de las personas representadas en la tabla del reporte
    reportadas_activas = sum(fila['activas'] for fila in filas)
    reportadas_inactivas = sum(fila['inactivas'] for fila in filas)

    # 9. Personas sin lugar de votación (campo NULL).
    # Se listan aquí para que el panel muestre quiénes son y enlaza al filtrado.
    sin_lugar_qs = (
        People.objects
        .filter(Q(lugar_votacion__isnull=True) | Q(lugar_votacion__exact=""))
    )
    total_sin_lugar = sin_lugar_qs.count()
    sin_lugar_inactivas = sin_lugar_qs.filter(activo=False).count()
    total_con_lugar = total_personas - total_sin_lugar
    porcentaje_sin_lugar = round(total_sin_lugar * 100 / total_personas) if total_personas else 0

    sin_lugar_lista = list(
        sin_lugar_qs
        .only('id', 'nombre', 'apellido', 'telefono', 'urbanizacion', 'activo', 'fecha_creacion')
        .order_by('-activo', 'nombre', 'apellido')
    )

    # Iniciales para el avatar de cada persona, en mayúsculas.
    for persona in sin_lugar_lista:
        persona.iniciales = (
            (persona.nombre.strip()[:1] + persona.apellido.strip()[:1]).upper()
            or '?'
        )

    sin_lugar = sin_lugar_lista[:10]
    sin_lugar_restantes = max(total_sin_lugar - len(sin_lugar), 0)

    context = {
        'page_title': 'Panel de Control',
        'page_subtitle': 'Bienvenido al sistema Luna',
        'total_users': total_usuarios,
        'total_personas': total_personas,
        'total_urbanizaciones': total_urbanizaciones,
        'total_referidos': total_referidos,
        'total_admins': total_admins,
        'total_activas': total_activas,
        'total_inactivas': total_inactivas,
        'porcentaje_activas': round(total_activas * 100 / total_personas) if total_personas else 0,
        'porcentaje_inactivas': round(total_inactivas * 100 / total_personas) if total_personas else 0,
        'filas': filas,
        'buscar': buscar,
        'tipo_actual': tipo,
        'total_lugares': len(filas),
        'total_lugares_urbanizacion': sum(1 for fila in filas if not fila['es_vereda']),
        'total_lugares_vereda': sum(1 for fila in filas if fila['es_vereda']),
        'reportadas_activas': reportadas_activas,
        'reportadas_inactivas': reportadas_inactivas,
        'total_sin_lugar': total_sin_lugar,
        'porcentaje_sin_lugar': porcentaje_sin_lugar,
        'total_con_lugar': total_con_lugar,
        'sin_lugar_inactivas': sin_lugar_inactivas,
        'sin_lugar': sin_lugar,
        'sin_lugar_restantes': sin_lugar_restantes,
    }

    return render(request, 'dashboard/dashboard.html', context)
