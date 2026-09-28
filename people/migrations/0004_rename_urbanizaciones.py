from django.db import migrations


RENOMBRES = {
    'Cascada': 'La Cascada',
    'Aurora': 'La Aurora',
    'San Cristóbal': 'Corregimiento de San Cristóbal',
}


def renombrar(apps, schema_editor):
    People = apps.get_model('people', 'People')
    for viejo, nuevo in RENOMBRES.items():
        People.objects.filter(urbanizacion=viejo).update(urbanizacion=nuevo)


def revertir(apps, schema_editor):
    People = apps.get_model('people', 'People')
    for viejo, nuevo in RENOMBRES.items():
        People.objects.filter(urbanizacion=nuevo).update(urbanizacion=viejo)


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_people_activo_alter_people_referido_por'),
    ]

    operations = [
        migrations.RunPython(renombrar, revertir),
    ]