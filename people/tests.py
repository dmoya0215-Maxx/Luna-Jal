from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.db.models import ProtectedError
from django.db import transaction
from django import forms
from django.core.exceptions import ValidationError

from people.models import People
from user.models import User


class DeactivateInsteadOfDeleteTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create(
            nombre='boss', contraseña='x', cargo='Admin'
        )
        self.referente = People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04121234567',
            edad=40, urbanizacion='Aurora',
        )
        self.referido = People.objects.create(
            nombre='Luis', apellido='Perez', telefono='04127654321',
            edad=30, urbanizacion='Aurora', referido_por=self.referente,
        )

    def login(self, user, rol):
        session = self.client.session
        session['logueado'] = {'id': user.id, 'nombre': user.nombre, 'rol': rol}
        session.save()

    def test_deactivate_keeps_referral_record(self):
        self.login(self.admin, 'Admin')

        url = reverse('deactivateperson', args=[self.referente.id])
        confirmacion = self.client.get(url)
        self.assertEqual(confirmacion.status_code, 200)
        self.assertContains(confirmacion, 'Ana Ramos')
        self.assertContains(confirmacion, 'Luis Perez')

        self.assertEqual(self.client.post(url).status_code, 302)
        self.referente.refresh_from_db()
        self.referido.refresh_from_db()

        self.assertFalse(self.referente.activo)
        self.assertEqual(People.objects.count(), 2)
        self.assertEqual(self.referido.referido_por_id, self.referente.id)

    def test_reactivate_restores(self):
        self.login(self.admin, 'Admin')

        self.referente.activo = False
        self.referente.save(update_fields=['activo'])

        resp = self.client.post(reverse('activateperson', args=[self.referente.id]))
        self.assertEqual(resp.status_code, 302)
        self.referente.refresh_from_db()
        self.assertTrue(self.referente.activo)

    def test_hard_delete_is_blocked_while_referred(self):
        with self.assertRaises(ProtectedError):
            with transaction.atomic():
                self.referente.delete()

        self.assertEqual(People.objects.count(), 2)
        self.assertEqual(self.referido.referido_por_id, self.referente.id)

    def test_inactive_people_stay_listed_and_marked(self):
        self.referente.activo = False
        self.referente.save(update_fields=['activo'])
        self.login(self.admin, 'Admin')

        resp = self.client.get(reverse('readperson'))
        self.assertContains(resp, 'Ana Ramos')
        self.assertContains(resp, 'row-inactive')
        self.assertContains(resp, 'Inactiva')
        self.assertContains(resp, 'Reactivar')

    def test_inactive_people_remain_referable(self):
        self.referente.activo = False
        self.referente.save(update_fields=['activo'])
        self.login(self.admin, 'Admin')

        resp = self.client.get(reverse('updateperson', args=[self.referido.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ana Ramos')

    def test_invitado_cannot_deactivate(self):
        invitado = User.objects.create(nombre='inv', contraseña='x', cargo='Invitado')
        self.login(invitado, 'Invitado')

        resp = self.client.post(reverse('deactivateperson', args=[self.referente.id]))
        self.assertEqual(resp.status_code, 403)
        self.referente.refresh_from_db()
        self.assertTrue(self.referente.activo)

    def test_delete_url_no_longer_exists(self):
        with self.assertRaises(NoReverseMatch):
            reverse('deleteperson', args=[self.referente.id])

class PersonVotacionFieldsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create(
            nombre='boss', contraseña='x', cargo='Admin'
        )

    def login(self):
        session = self.client.session
        session['logueado'] = {
            'id': self.admin.id, 'nombre': self.admin.nombre, 'rol': 'Admin'
        }
        session.save()

    def datos(self, **extra):
        base = {
            'nombre': 'Ana',
            'apellido': 'Ramos',
            'telefono': '04121234567',
            'correo': 'ana@example.com',
            'edad': '40',
            'urbanizacion': 'La Aurora',
            'lugar_votacion': '',
            'mesa_votacion': '',
            'referido_por': '',
        }
        base.update(extra)
        return base

    # ------------------------------------------------- Campos de texto, sin selectores

    def test_los_campos_son_de_texto_y_opcionales(self):
        self.login()

        resp = self.client.get(reverse('createperson'))
        self.assertEqual(resp.status_code, 200)

        form = resp.context['form']
        for campo in ('lugar_votacion', 'mesa_votacion'):
            self.assertFalse(form.fields[campo].required)
            self.assertIsInstance(form.fields[campo].widget, forms.TextInput)

        html = resp.content.decode('utf-8')
        self.assertIn('name="lugar_votacion"', html)
        self.assertIn('name="mesa_votacion"', html)
        # No debe haber ningún selector para estos campos.
        self.assertNotIn('<select name="lugar_votacion"', html)
        self.assertNotIn('<select name="mesa_votacion"', html)

    def test_enviar_formulario_sin_lugar_guarda_null(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos())
        self.assertEqual(resp.status_code, 302)

        persona = People.objects.get(nombre='Ana')
        self.assertIsNone(persona.lugar_votacion)
        self.assertIsNone(persona.mesa_votacion)

    def test_espacios_en_blanco_se_guardan_como_null(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos(
            lugar_votacion='   ', mesa_votacion='  '
        ))
        self.assertEqual(resp.status_code, 302)

        persona = People.objects.get(nombre='Ana')
        self.assertIsNone(persona.lugar_votacion)
        self.assertIsNone(persona.mesa_votacion)

    def test_lugar_asignado_sin_mesa(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos(
            lugar_votacion='Escuela Juan Pablo II'
        ))
        self.assertEqual(resp.status_code, 302)

        persona = People.objects.get(nombre='Ana')
        self.assertEqual(persona.lugar_votacion, 'Escuela Juan Pablo II')
        self.assertIsNone(persona.mesa_votacion)

    def test_lugar_y_mesa_asignados(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos(
            lugar_votacion='Escuela Juan Pablo II',
            mesa_votacion='Mesa 001',
        ))
        self.assertEqual(resp.status_code, 302)

        persona = People.objects.get(nombre='Ana')
        self.assertEqual(persona.lugar_votacion, 'Escuela Juan Pablo II')
        self.assertEqual(persona.mesa_votacion, 'Mesa 001')

    def test_el_texto_se_guarda_recortado(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos(
            lugar_votacion='  Escuela Central  ',
            mesa_votacion='  Mesa 12  ',
        ))
        self.assertEqual(resp.status_code, 302)

        persona = People.objects.get(nombre='Ana')
        self.assertEqual(persona.lugar_votacion, 'Escuela Central')
        self.assertEqual(persona.mesa_votacion, 'Mesa 12')

    def test_cualquier_texto_es_valido_sin_catalogo(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos(
            lugar_votacion='Puesto 44 - Av. principal',
            mesa_votacion='Mesa Z-9',
        ))
        self.assertEqual(resp.status_code, 302)

        persona = People.objects.get(nombre='Ana')
        self.assertEqual(persona.lugar_votacion, 'Puesto 44 - Av. principal')
        self.assertEqual(persona.mesa_votacion, 'Mesa Z-9')

    # ------------------------------------------------- Validaciones de integridad

    def test_mesa_sin_lugar_es_rechazada(self):
        self.login()

        resp = self.client.post(reverse('createperson'), self.datos(
            lugar_votacion='',
            mesa_votacion='Mesa 001',
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            'mesa_votacion',
            resp.context['form'].errors
        )
        self.assertContains(
            resp, 'Indique primero el lugar de votación para asignar una mesa'
        )
        self.assertFalse(People.objects.filter(nombre='Ana').exists())

    def test_editar_puede_borrar_el_lugar_y_deja_la_mesa_en_null(self):
        self.login()
        persona = People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04121234567', edad=40,
            urbanizacion='La Aurora', lugar_votacion='Escuela Central',
            mesa_votacion='Mesa 12',
        )

        resp = self.client.post(reverse('updateperson', args=[persona.id]), self.datos(
            lugar_votacion='', mesa_votacion=''
        ))
        self.assertEqual(resp.status_code, 302)

        persona.refresh_from_db()
        self.assertIsNone(persona.lugar_votacion)
        self.assertIsNone(persona.mesa_votacion)

    def test_editar_puede_cambiar_el_lugar_y_la_mesa(self):
        self.login()
        persona = People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04121234567', edad=40,
            urbanizacion='La Aurora', lugar_votacion='Escuela Central',
            mesa_votacion='Mesa 12',
        )

        resp = self.client.post(reverse('updateperson', args=[persona.id]), self.datos(
            lugar_votacion='Colegio Norte', mesa_votacion='Mesa 3'
        ))
        self.assertEqual(resp.status_code, 302)

        persona.refresh_from_db()
        self.assertEqual(persona.lugar_votacion, 'Colegio Norte')
        self.assertEqual(persona.mesa_votacion, 'Mesa 3')

    def test_el_modelo_rechaza_mesa_sin_lugar(self):
        persona = People(
            nombre='Ana', apellido='Ramos', telefono='04121234567', edad=40,
            urbanizacion='La Aurora', mesa_votacion='Mesa 001',
        )
        with self.assertRaises(ValidationError):
            persona.full_clean()


class FiltroSinLugarVotacionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create(
            nombre='boss', contraseña='x', cargo='Admin'
        )

        self.con_lugar = People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04120000001', edad=40,
            urbanizacion='La Aurora', lugar_votacion='Escuela Juan Pablo II',
            mesa_votacion='Mesa 001',
        )
        self.sin_lugar_1 = People.objects.create(
            nombre='Luis', apellido='Perez', telefono='04120000002', edad=30,
            urbanizacion='La Aurora',
        )
        self.sin_lugar_2 = People.objects.create(
            nombre='Maria', apellido='Gomez', telefono='04120000003', edad=25,
            urbanizacion='La Aurora', activo=False,
        )

    def login(self):
        session = self.client.session
        session['logueado'] = {
            'id': self.admin.id, 'nombre': self.admin.nombre, 'rol': 'Admin'
        }
        session.save()

    def test_contador_de_personas_sin_lugar(self):
        self.login()

        resp = self.client.get(reverse('readperson'))
        self.assertEqual(resp.context['total_sin_lugar'], 2)
        self.assertContains(resp, 'Solo sin lugar (2)')

    def test_filtro_sin_asignar_devuelve_solo_las_null(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'lugar_votacion': 'sin_asignar'})
        self.assertEqual(resp.status_code, 200)

        personas = list(resp.context['person'])
        self.assertEqual(len(personas), 2)
        self.assertIn(self.sin_lugar_1, personas)
        self.assertIn(self.sin_lugar_2, personas)
        self.assertNotIn(self.con_lugar, personas)

        self.assertContains(resp, 'Luis Perez')
        self.assertContains(resp, 'Maria Gomez')
        self.assertContains(resp, 'sin lugar de votación')

    def test_filtro_por_nombre_de_lugar(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {
            'lugar_votacion': 'Escuela Juan Pablo II'
        })
        self.assertEqual(list(resp.context['person']), [self.con_lugar])
        # El contador global no cambia por filtrar.
        self.assertEqual(resp.context['total_sin_lugar'], 2)

    def test_filtro_de_lugar_ignora_mayusculas(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {
            'lugar_votacion': 'escuela juan pablo ii'
        })
        self.assertEqual(list(resp.context['person']), [self.con_lugar])

    def test_filtro_lugar_inexistente_no_devuelve_nada(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'lugar_votacion': 'No Existe'})
        self.assertEqual(list(resp.context['person']), [])

    def test_sin_filtro_lista_todas(self):
        self.login()

        resp = self.client.get(reverse('readperson'))
        self.assertEqual(resp.context['person'].count(), 3)

    def test_tabla_muestra_sin_lugar(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'lugar_votacion': 'sin_asignar'})
        self.assertContains(resp, 'Sin lugar')
        self.assertNotContains(resp, 'Mesa 001')

    def test_tabla_muestra_lugar_y_mesa_cuando_existen(self):
        self.login()

        resp = self.client.get(reverse('readperson'))
        self.assertContains(resp, 'Escuela Juan Pablo II')
        self.assertContains(resp, 'Mesa 001')

    def test_sin_filtro_de_lugar_se_revierte_al_limpiar(self):
        self.login()

        resp = self.client.get(reverse('readperson'))
        self.assertEqual(resp.context['lugar_actual'], '')
        self.assertEqual(resp.context['person'].count(), 3)

class BuscarPersonaPorNombreTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create(
            nombre='boss', contraseña='x', cargo='Admin'
        )
        self.ana = People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04120000001', edad=40,
            urbanizacion='La Aurora',
        )
        self.luis = People.objects.create(
            nombre='Luis', apellido='Perez', telefono='04120000002', edad=30,
            urbanizacion='La Aurora',
        )
        self.maria = People.objects.create(
            nombre='Maria', apellido='Gomez', telefono='04120000003', edad=25,
            urbanizacion='La Aurora',
        )

    def login(self):
        session = self.client.session
        session['logueado'] = {
            'id': self.admin.id, 'nombre': self.admin.nombre, 'rol': 'Admin'
        }
        session.save()

    def test_el_formulario_tiene_campo_de_busqueda_por_nombre(self):
        self.login()

        resp = self.client.get(reverse('readperson'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'name="buscar"')
        self.assertContains(resp, 'Buscar persona')

    def test_busca_por_nombre(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'buscar': 'Ana'})
        self.assertEqual(list(resp.context['person']), [self.ana])
        self.assertEqual(resp.context['buscar'], 'Ana')

    def test_busca_por_apellido(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'buscar': 'Gomez'})
        self.assertEqual(list(resp.context['person']), [self.maria])

    def test_la_busqueda_ignora_mayusculas(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'buscar': 'luis'})
        self.assertEqual(list(resp.context['person']), [self.luis])

    def test_busqueda_parcial_en_el_nombre(self):
        self.login()

        # Solo "Ramos" contiene "ram".
        resp = self.client.get(reverse('readperson'), {'buscar': 'ram'})
        self.assertEqual(list(resp.context['person']), [self.ana])

        # "e" aparece en "Perez" y en "Gomez".
        resp = self.client.get(reverse('readperson'), {'buscar': 'e'})
        self.assertEqual(
            sorted(p.nombre for p in resp.context['person']),
            ['Luis', 'Maria'],
        )

    def test_busqueda_sin_resultados(self):
        self.login()

        resp = self.client.get(reverse('readperson'), {'buscar': 'Zzz'})
        self.assertEqual(list(resp.context['person']), [])

    def test_busqueda_se_combina_con_el_filtro_de_lugar(self):
        self.login()
        self.luis.lugar_votacion = 'Escuela Central'
        self.luis.save()

        resp = self.client.get(reverse('readperson'), {
            'buscar': 'Luis', 'lugar_votacion': 'sin_asignar'
        })
        self.assertEqual(list(resp.context['person']), [])

        resp = self.client.get(reverse('readperson'), {
            'buscar': 'Luis', 'lugar_votacion': 'Escuela Central'
        })
        self.assertEqual(list(resp.context['person']), [self.luis])
