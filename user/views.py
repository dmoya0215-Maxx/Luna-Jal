from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import check_password
from .decorators import admin_required, cannot_delete_admins, login_required_custom
from .form import UserForm
from .models import User
import time

MAX_INTENTOS_LOGIN = 5
BLOQUEO_SEGUNDOS = 300


def login_view(request):
    if request.method == "POST":
        # Control de fuerza bruta: intentos fallidos registrados en la sesión
        intentos = int(request.session.get("login_intentos", 0))
        bloqueado_hasta = request.session.get("login_bloqueado_hasta", 0)
        if bloqueado_hasta and int(bloqueado_hasta) > int(time.time()):
            restante = int(bloqueado_hasta) - int(time.time())
            messages.error(
                request,
                f"Demasiados intentos fallidos. Intenta de nuevo en {restante} segundos."
            )
            return redirect('login')

        usuario = request.POST.get("user", "").strip()
        contra = request.POST.get("clave", "")
        try:
            # Paso 1: Buscar usuario por nombre
            user = User.objects.get(nombre=usuario)

            # Paso 2: Verificar contraseña usando check_password()
            if user.check_password(contra):
                # Regenerar la sesión para evitar fijación de sesión
                request.session.cycle_key()
                request.session["login_intentos"] = 0
                request.session.pop("login_bloqueado_hasta", None)
                messages.success(request, "Bienvenido al sistema")
                request.session["logueado"] = {
                    "id": user.id,
                    "nombre": f"{user.nombre}",
                    "rol": user.cargo
                }
                return redirect("dashboard")
            else:
                # Contraseña incorrecta
                intentos += 1
                if intentos >= MAX_INTENTOS_LOGIN:
                    request.session["login_intentos"] = 0
                    request.session["login_bloqueado_hasta"] = int(time.time()) + BLOQUEO_SEGUNDOS
                    messages.error(
                        request,
                        "Demasiados intentos fallidos. Cuenta bloqueada temporalmente."
                    )
                else:
                    request.session["login_intentos"] = intentos
                    messages.error(request, "Usuario o contraseña incorrecto")
                return redirect('login')

        except User.DoesNotExist:
            # Usuario no existe
            intentos += 1
            if intentos >= MAX_INTENTOS_LOGIN:
                request.session["login_intentos"] = 0
                request.session["login_bloqueado_hasta"] = int(time.time()) + BLOQUEO_SEGUNDOS
                messages.error(
                    request,
                    "Demasiados intentos fallidos. Cuenta bloqueada temporalmente."
                )
            else:
                request.session["login_intentos"] = intentos
                messages.error(request, "Usuario o contraseña incorrecto")
            return redirect('login')
    else:
        if request.session.get("logueado", False):
            return redirect('dashboard')
        else:
            return render(request, "user/login.html")

@login_required_custom
def ReadUser(request):
    user = User.objects.all().order_by('id')
    return render(request, 'user/readuser.html', {
        'user': user,
        'page_title': 'Gestión de Usuarios',
        'page_subtitle': 'Administra los usuarios del sistema'
    })


@login_required_custom
@admin_required
def CreateUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('user')
    else:
        form = UserForm()
    users = User.objects.all().order_by('id')
    return render(request, 'user/createuser.html', {
        'form': form,
        'user': users,
        'page_title': 'Crear Nuevo Usuario',
        'page_subtitle': 'Agrega un nuevo usuario al sistema'
    })


@login_required_custom
@admin_required
def UpdateUser(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente')
            return redirect('user')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/updateuser.html', {
        'form': form,
        'user': user,
        'page_title': 'Editar Usuario',
        'page_subtitle': f'Actualizando: {user.nombre}'
    })


@login_required_custom
@admin_required
@cannot_delete_admins
def DeleteUser(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente')
        return redirect('user')
    return render(request, 'user/deleteuser.html', {
        'user': user,
        'page_title': 'Eliminar Usuario',
        'page_subtitle': 'Esta acción es irreversible'
    })

def logout_view(request):
    logueado = request.session.get("logueado")
    if logueado:
        request.session.flush()
    messages.success(request, "Sesion cerrada")
    return redirect('login')