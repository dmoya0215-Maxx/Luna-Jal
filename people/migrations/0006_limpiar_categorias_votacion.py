from django.db import migrations


def limpiar_estructura_votacion(apps, schema_editor):
    """Retira el esquema de catálogos que se descartó.

    Los campos de votación pasaron de ser FK a texto libre, así que las columnas
    *_id y las tablas votacion_* quedan huérfanas. Se eliminan solo si existen,
    para que la migración sea segura tanto en bases nuevas como en las que
    aplicaron la versión anterior con catálogos.
    """
    conexion = schema_editor.connection
    tablas = set(conexion.introspection.table_names())
    quote = conexion.ops.quote_name

    with conexion.cursor() as cursor:
        # 1. Quitar las constraints FK: MySQL no permite eliminar una columna
        #    que participa en una llave foránea.
        if 'votacion_lugarvotacion' in tablas or 'votacion_mesavotacion' in tablas:
            cursor.execute(
                """
                SELECT kcu.CONSTRAINT_NAME
                FROM information_schema.KEY_COLUMN_USAGE AS kcu
                JOIN information_schema.REFERENTIAL_CONSTRAINTS AS rc
                  ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                 AND rc.CONSTRAINT_SCHEMA = kcu.CONSTRAINT_SCHEMA
                WHERE kcu.TABLE_SCHEMA = DATABASE()
                  AND kcu.TABLE_NAME = 'people_people'
                  AND kcu.REFERENCED_TABLE_NAME IN
                      ('votacion_lugarvotacion', 'votacion_mesavotacion')
                """
            )
            for (constraint,) in cursor.fetchall():
                cursor.execute(
                    f'ALTER TABLE {quote("people_people")} '
                    f'DROP FOREIGN KEY {quote(constraint)}'
                )

        # 2. Eliminar las columnas *_id que quedaron sin uso.
        existentes = {
            c.name for c in conexion.introspection.get_table_description(
                cursor, 'people_people'
            )
        }
        for columna in ('lugar_votacion_id', 'mesa_votacion_id'):
            if columna in existentes:
                cursor.execute(
                    f'ALTER TABLE {quote("people_people")} '
                    f'DROP COLUMN {quote(columna)}'
                )

        # 3. Retirar las tablas del catálogo, ya sin referencias.
        for tabla in ('votacion_mesavotacion', 'votacion_lugarvotacion'):
            if tabla in tablas:
                cursor.execute(f'DROP TABLE IF EXISTS {quote(tabla)}')


def restaurar_estructura_votacion(apps, schema_editor):
    """No-op: el rollback solo restaura el estado de Django, no el esquema viejo."""


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_people_lugar_votacion_people_mesa_votacion'),
    ]

    operations = [
        migrations.RunPython(
            limpiar_estructura_votacion,
            restaurar_estructura_votacion,
        ),
    ]
