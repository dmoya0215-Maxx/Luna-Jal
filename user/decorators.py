from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import User


def get_session_user(request):
    session_user = request.session.get("logueado")
    if isinstance(session_user, dict):
        return session_user
    return {}


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not get_session_user(request):
            messages.warning(request, "Debes iniciar sesión para acceder a esta sección")
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        session_user = get_session_user(request)

        if not session_user:
            messages.warning(request, "Debes iniciar sesión para acceder a esta sección")
            return redirect('login')

        if str(session_user.get('rol', '')).strip().lower() != 'admin':
            messages.error(request, "No tienes permisos para realizar esta acción")

            path = request.path.lower().strip('/')
            if path.startswith('person'):
                return redirect('readperson')
            if path.startswith('user'):
                return redirect('user')
            return redirect('dashboard')

        return view_func(request, *args, **kwargs)

    return wrapper


def cannot_delete_admins(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id is None and len(args) > 0:
            user_id = args[0]
        if user_id is None:
            user_id = request.POST.get('id')

        if user_id is not None:
            user_to_delete = get_object_or_404(User, id=user_id)
            if str(user_to_delete.cargo).strip().lower() == 'admin':
                messages.error(request, "No se pueden eliminar usuarios administradores")
                return redirect('user')

        return view_func(request, *args, **kwargs)

    return wrapper
