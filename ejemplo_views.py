"""
Ejemplo de vistas Django para el sistema web responsive
Coloca este código en tu archivo views.py
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de login con validación y manejo de errores
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Aquí puedes usar User.objects.get(email=email) si tienes ese campo
        # O usar username si usas el modelo de usuario por defecto
        try:
            # Intenta autenticación con email
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
                return redirect('dashboard')  # Cambia 'dashboard' por tu URL de dashboard
            else:
                messages.error(request, 'Email o contraseña inválidos')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_view(request):
    """
    Vista del dashboard - solo para usuarios autenticados
    """
    context = {
        'user': request.user,
        # Aquí puedes añadir datos adicionales que quieras mostrar en el dashboard
    }
    return render(request, 'dashboard.html', context)


def logout_view(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('login')


# URLs de ejemplo - añade esto a tu urls.py:
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
"""
