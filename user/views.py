from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import check_password
from .decorators import admin_required, login_required_custom
from .form import UserForm
from .models import User

def login_view(request):
    if request.method == "POST":
        print("LLEGÓ AL LOGIN")
        print(request.POST)
        usuario = request.POST.get("user", "").strip()
        contra = request.POST.get("clave", "")
        try:
            # Paso 1: Buscar usuario por nombre
            user = User.objects.get(nombre=usuario)

            # Paso 2: Verificar contraseña usando check_password()
            if user.check_password(contra):
                messages.success(request, "Bienvenido al sistema")
                request.session["logueado"] = {
                    "id": user.id,
                    "nombre": f"{user.nombre}",
                    "rol": user.cargo
                }
                return redirect("dashboard")
            else:
                # Contraseña incorrecta
                messages.error(request, "Usuario o contraseña incorrecto")
                request.session["logueado"] = None
                return redirect('login')
                
        except User.DoesNotExist:
            # Usuario no existe
            messages.error(request, "Usuario o contraseña incorrecto")
            request.session["logueado"] = None
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