from django.conf import settings
from django.shortcuts import render


def _permitido_preview(request):
    """Permite previsualizar errores en desarrollo o a usuarios admin."""
    sesion = request.session.get("logueado")
    return (
        settings.DEBUG
        or (isinstance(sesion, dict) and str(sesion.get('rol', '')).strip().lower() == 'admin')
    )


def error_400(request, exception=None):
    """Error 400: Solicitud no válida."""
    return render(request, 'errors/400.html', {
        'page_title': 'Solicitud no válida'
    }, status=400)


def error_403(request, exception=None):
    """Error 403: Acceso denegado."""
    return render(request, 'errors/403.html', {
        'page_title': 'Acceso denegado'
    }, status=403)


def error_404(request, exception=None):
    """Error 404: Página no encontrada."""
    return render(request, 'errors/404.html', {
        'page_title': 'Página no encontrada'
    }, status=404)


def error_500(request):
    """Error 500: Error interno del servidor."""
    return render(request, 'errors/500.html', {
        'page_title': 'Error interno del servidor'
    }, status=500)


# --- Vistas de previsualización (desarrollo o admin) ---

def view_error_400(request):
    if not _permitido_preview(request):
        return error_404(request)
    return error_400(request)


def view_error_403(request):
    if not _permitido_preview(request):
        return error_404(request)
    return error_403(request)


def view_error_404(request):
    if not _permitido_preview(request):
        return error_404(request)
    return error_404(request)


def view_error_500(request):
    if not _permitido_preview(request):
        return error_404(request)
    return error_500(request)