from django.db import migrations, models


def agregar_columnas_si_faltan(apps, schema_editor):
    """Crea lugar_votacion y mesa_votacion solo si aún no existen.

    Necesaria porque el 0005 original era la versión con claves foráneas:
    en bases que ya lo aplicaron, Django da el AddField por hecho y las columnas
    de texto nunca llegan a crearse.
    """
    conexion = schema_editor.connection
    quote = conexion.ops.quote_name

    with conexion.cursor() as cursor:
        existentes = {
            c.name for c in conexion.introspection.get_table_description(
                cursor, 'people_people'
            )
        }

        if 'lugar_votacion' not in existentes:
            cursor.execute(
                f'ALTER TABLE {quote("people_people")} '
                'ADD COLUMN `lugar_votacion` varchar(150) NULL'
            )

        if 'mesa_votacion' not in existentes:
            cursor.execute(
                f'ALTER TABLE {quote("people_people")} '
                'ADD COLUMN `mesa_votacion` varchar(100) NULL'
            )


def quitar_columnas(apps, schema_editor):
    conexion = schema_editor.connection
    quote = conexion.ops.quote_name
    with conexion.cursor() as cursor:
        existentes = {
            c.name for c in conexion.introspection.get_table_description(
                cursor, 'people_people'
            )
        }
        for columna in ('lugar_votacion', 'mesa_votacion'):
            if columna in existentes:
                cursor.execute(
                    f'ALTER TABLE {quote("people_people")} '
                    f'DROP COLUMN {quote(columna)}'
                )


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_limpiar_categorias_votacion'),
    ]

    operations = [
        migrations.RunPython(agregar_columnas_si_faltan, quitar_columnas),
        migrations.AlterField(
            model_name='people',
            name='lugar_votacion',
            field=models.CharField(
                blank=True,
                help_text='Opcional. Si se deja vacío se guarda sin valor (NULL).',
                max_length=150,
                null=True,
                verbose_name='Lugar de votación',
            ),
        ),
        migrations.AlterField(
            model_name='people',
            name='mesa_votacion',
            field=models.CharField(
                blank=True,
                help_text='Opcional. Requiere un lugar de votación.',
                max_length=100,
                null=True,
                verbose_name='Mesa de votación',
            ),
        ),
    ]
