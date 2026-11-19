from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_asegurar_columnas_votacion'),
    ]

    operations = [
        UnaccentExtension(),
    ]
