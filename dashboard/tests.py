from django.test import TestCase
from django.urls import reverse

from people.models import People
from user.models import User


class DashboardPersonasTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create(
            nombre='boss', contraseña='x', cargo='Admin'
        )
        # Cantares V: 10 activas + 5 inactivas
        for i in range(10):
            People.objects.create(
                nombre=f'Activa{i}', apellido='Cantares', telefono=f'04120000{i:02d}',
                edad=30, urbanizacion='Cantares V',
            )
        for i in range(5):
            People.objects.create(
                nombre=f'Inactiva{i}', apellido='Cantares', telefono=f'04130000{i:02d}',
                edad=30, urbanizacion='Cantares V', activo=False,
            )
        # Vereda con 2 activas + 1 inactiva
        for i in range(2):
            People.objects.create(
                nombre=f'Vereda{i}', apellido='Boqueron', telefono=f'04140000{i:02d}',
                edad=30, urbanizacion='S.C Boquerón',
            )
        People.objects.create(
            nombre='VeredaInactiva', apellido='Boqueron', telefono='04149999',
            edad=30, urbanizacion='S.C Boquerón', activo=False,
        )

    def login(self, rol='Admin'):
        session = self.client.session
        session['logueado'] = {'id': self.admin.id, 'nombre': self.admin.nombre, 'rol': rol}
        session.save()

    def test_dashboard_counts_activas_and_inactivas_per_place(self):
        self.login()

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Cantares V')
        self.assertContains(resp, 'S.C Boquerón')

        filas = {fila['nombre']: fila for fila in resp.context['filas']}
        self.assertEqual(filas['Cantares V']['activas'], 10)
        self.assertEqual(filas['Cantares V']['inactivas'], 5)
        self.assertEqual(filas['Cantares V']['total'], 15)
        self.assertEqual(filas['Cantares V']['porcentaje_activas'], 67)
        self.assertFalse(filas['Cantares V']['es_vereda'])
        self.assertTrue(filas['S.C Boquerón']['es_vereda'])
        self.assertEqual(filas['S.C Boquerón']['activas'], 2)
        self.assertEqual(filas['S.C Boquerón']['inactivas'], 1)

    def test_dashboard_global_activas_and_inactivas(self):
        self.login()

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.context['total_activas'], 12)
        self.assertEqual(resp.context['total_inactivas'], 6)
        self.assertEqual(resp.context['total_personas'], 18)
        self.assertEqual(resp.context['porcentaje_activas'], 67)
        self.assertEqual(resp.context['porcentaje_inactivas'], 33)

    def test_dashboard_groups_urbanizaciones_and_veredas(self):
        self.login()

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.context['total_lugares'], 2)
        self.assertEqual(resp.context['total_lugares_urbanizacion'], 1)
        self.assertEqual(resp.context['total_lugares_vereda'], 1)
        self.assertEqual(resp.context['reportadas_activas'], 12)
        self.assertEqual(resp.context['reportadas_inactivas'], 6)
        self.assertEqual(resp.context['total_urbanizaciones'], 2)

    def test_dashboard_filters_by_tipo(self):
        self.login()

        solo_veredas = self.client.get(reverse('dashboard'), {'tipo': 'vereda'})
        self.assertEqual(len(solo_veredas.context['filas']), 1)
        self.assertEqual(solo_veredas.context['reportadas_activas'], 2)
        self.assertEqual(solo_veredas.context['reportadas_inactivas'], 1)
        self.assertEqual(solo_veredas.context['total_lugares'], 1)

        solo_urbanizaciones = self.client.get(reverse('dashboard'), {'tipo': 'urbanizacion'})
        self.assertEqual(len(solo_urbanizaciones.context['filas']), 1)
        self.assertEqual(solo_urbanizaciones.context['reportadas_activas'], 10)
        self.assertEqual(solo_urbanizaciones.context['reportadas_inactivas'], 5)

    def test_dashboard_search_by_place_name(self):
        self.login()

        resp = self.client.get(reverse('dashboard'), {'buscar': 'boqueron'})
        self.assertEqual(len(resp.context['filas']), 1)
        self.assertEqual(resp.context['filas'][0]['nombre'], 'S.C Boquerón')

    def test_dashboard_row_link_filters_person_list(self):
        self.login()

        resp = self.client.get(reverse('dashboard'))
        url = reverse('readperson')
        filtrada = self.client.get(url, {'urbanizacion': 'Cantares V'})
        self.assertEqual(filtrada.context['urbanizacion_actual'], 'Cantares V')
        self.assertEqual(filtrada.context['total_activas'], 10)
        self.assertEqual(filtrada.context['total_inactivas'], 5)
        self.assertContains(resp, url)

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 403)

class DashboardSinLugarVotacionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create(
            nombre='boss', contraseña='x', cargo='Admin'
        )
        People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04120000001', edad=40,
            urbanizacion='La Aurora', lugar_votacion='Escuela Central',
        )
        People.objects.create(
            nombre='Luis', apellido='Perez', telefono='04120000002', edad=30,
            urbanizacion='La Aurora',
        )
        People.objects.create(
            nombre='Maria', apellido='Gomez', telefono='04120000003', edad=25,
            urbanizacion='La Aurora',
        )

    def login(self):
        session = self.client.session
        session['logueado'] = {
            'id': self.admin.id, 'nombre': self.admin.nombre, 'rol': 'Admin'
        }
        session.save()

    def test_dashboard_cuenta_y_lista_las_personas_sin_lugar(self):
        self.login()

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['total_sin_lugar'], 2)
        self.assertEqual(resp.context['porcentaje_sin_lugar'], 67)

        nombres = [p.nombre for p in resp.context['sin_lugar']]
        self.assertEqual(nombres, ['Luis', 'Maria'])

        self.assertContains(resp, 'SIN LUGAR DE VOTACI')
        self.assertContains(resp, 'Personas sin lugar de votaci')
        self.assertContains(resp, 'Luis Perez')
        self.assertContains(resp, 'Maria Gomez')
        self.assertNotContains(resp, 'Ana Ramos')

    def test_dashboard_enlaza_al_listado_filtrado(self):
        self.login()

        resp = self.client.get(reverse('dashboard'))
        self.assertContains(resp, 'lugar_votacion=sin_asignar')

    def test_porcentaje_cero_sin_personas(self):
        self.login()
        People.objects.all().delete()

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.context['total_sin_lugar'], 0)
        self.assertEqual(resp.context['porcentaje_sin_lugar'], 0)

class DashboardPanelPendientesTests(TestCase):
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

    def test_panel_muestra_metricas_e_iniciales(self):
        self.login()
        People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04120000001', edad=40,
            urbanizacion='La Aurora',
        )
        People.objects.create(
            nombre='Luis', apellido='Perez', telefono='04120000002', edad=30,
            urbanizacion='La Aurora', activo=False,
        )
        People.objects.create(
            nombre='Maria', apellido='Gomez', telefono='04120000003', edad=25,
            urbanizacion='La Aurora',
        )
        People.objects.create(
            nombre='Pedro', apellido='Rios', telefono='04120000004', edad=50,
            urbanizacion='La Aurora', lugar_votacion='Escuela Central',
        )

        resp = self.client.get(reverse('dashboard'))
        ctx = resp.context

        self.assertEqual(ctx['total_sin_lugar'], 3)
        self.assertEqual(ctx['total_con_lugar'], 1)
        self.assertEqual(ctx['sin_lugar_inactivas'], 1)
        self.assertEqual(ctx['porcentaje_sin_lugar'], 75)

        iniciales = sorted(p.iniciales for p in ctx['sin_lugar'])
        self.assertEqual(iniciales, ['AR', 'LP', 'MG'])

        html = resp.content.decode('utf-8')
        self.assertIn('panel-pending', html)
        self.assertIn('pending-metrics', html)
        self.assertIn('pending-list', html)
        self.assertIn('avatar-ini', html)
        self.assertIn('>AR<', html)
        self.assertContains(resp, 'Pedro Rios', count=0)
        # Las activas se listan antes que las inactivas.
        activos = [p.nombre for p in ctx['sin_lugar'] if p.activo]
        self.assertEqual(activos, ['Ana', 'Maria'])

    def test_panel_lista_hasta_diez_y_avisa_del_resto(self):
        self.login()
        for i in range(14):
            People.objects.create(
                nombre='Persona', apellido=str(i).zfill(2),
                telefono='0412000%04d' % i, edad=30, urbanizacion='La Aurora',
            )

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(len(resp.context['sin_lugar']), 10)
        self.assertEqual(resp.context['sin_lugar_restantes'], 4)
        self.assertContains(resp, 'y 4 personas m')

    def test_panel_en_estado_al_dia_sin_pendientes(self):
        self.login()
        People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04120000001', edad=40,
            urbanizacion='La Aurora', lugar_votacion='Escuela Central',
        )

        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.context['total_sin_lugar'], 0)
        self.assertEqual(resp.context['porcentaje_sin_lugar'], 0)

        html = resp.content.decode('utf-8')
        self.assertIn('is-clear', html)
        self.assertIn('panel-empty', html)
        self.assertIn('Ninguna persona se registro sin lugar', html)
        self.assertNotIn('pending-list', html)
