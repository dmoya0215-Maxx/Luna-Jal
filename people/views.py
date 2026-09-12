from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from user.decorators import admin_required, login_required_custom
from .models import People
from .form import PersonForm

@login_required_custom
def ReadPerson(request):
    buscar = request.GET.get('buscar', '').strip()
    urbanizacion = request.GET.get('urbanizacion', '').strip()
    referido_por = request.GET.get('referido_por', '').strip()

    person = People.objects.all().order_by('id')

    # Buscador general
    if buscar:
        person = person.filter(
            models.Q(nombre__icontains=buscar) |
            models.Q(apellido__icontains=buscar) |
            models.Q(telefono__icontains=buscar) |
            models.Q(correo__icontains=buscar) |
            models.Q(urbanizacion__icontains=buscar)
        )

    # Filtro por urbanización
    if urbanizacion:
        person = person.filter(
            urbanizacion=urbanizacion
        )

    # Filtro por persona que lo refirió
    if referido_por and referido_por.isdigit():
        person = person.filter(
            referido_por_id=referido_por
        )
    elif referido_por:
        # Valor no numérico: no coincide con ningún registro
        person = person.none()

    # Opciones para los filtros
    urbanizaciones = (
        People.objects
        .values_list('urbanizacion', flat=True)
        .distinct()
        .order_by('urbanizacion')
    )

    personas_referentes = (
        People.objects
        .filter(referidos__isnull=False)
        .distinct()
        .order_by('nombre', 'apellido')
    )

    return render(request, 'person/readperson.html', {
        'person': person,
        'buscar': buscar,
        'urbanizacion_actual': urbanizacion,
        'referido_actual': referido_por,
        'urbanizaciones': urbanizaciones,
        'personas_referentes': personas_referentes,
        'page_title': 'Gestión de Personas',
        'page_subtitle': 'Administra el registro de personas'
    })

@login_required_custom

def CreatePerson(request):
    if request.method == "POST":
        person = PersonForm(request.POST)
        if person.is_valid():
            person.save()
            messages.success(request, 'Persona creada correctamente')
            return redirect ('readperson')
    else:
        person = PersonForm()
    return render (request, 'person/createperson.html', {
        'form': person,
        'page_title': 'Registrar Nueva Persona',
        'page_subtitle': 'Complete el formulario para agregar una persona'
    })

@login_required_custom

def UpdatePerson(request, id):
    person = get_object_or_404(People, id=id)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Persona actualizada correctamente')
            return redirect ('readperson')
    else:
        form = PersonForm(instance=person)
    return render(request, 'person/updateperson.html', {
        'form': form,
        'object': person,
        'page_title': 'Editar Persona',
        'page_subtitle': f'Actualizando: {person.nombre}'
    })

@login_required_custom
@admin_required
def DeletePerson(request, id):
    person = get_object_or_404(People, id=id)
    if request.method == "POST":
        person.delete()
        messages.success(request, 'Persona eliminada correctamente')
        return redirect ('readperson')
    return render(request, 'person/deleteperson.html', {
        'person': person,
        'page_title': 'Eliminar Persona',
        'page_subtitle': 'Esta acción es irreversible'
    })