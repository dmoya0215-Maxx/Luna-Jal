from django.test import TestCase

from api.serializers import PeopleSerializer
from people.models import People


class PeopleSerializerVotacionTests(TestCase):
    def setUp(self):
        self.datos = {
            'nombre': 'Ana',
            'apellido': 'Ramos',
            'telefono': '04121234567',
            'correo': 'ana@example.com',
            'edad': 40,
            'urbanizacion': 'La Aurora',
        }

    def test_serializer_expone_los_campos_nuevos(self):
        campos = PeopleSerializer().fields
        self.assertIn('lugar_votacion', campos)
        self.assertIn('mesa_votacion', campos)
        self.assertFalse(campos['lugar_votacion'].required)
        self.assertFalse(campos['mesa_votacion'].required)

    def test_sin_lugar_es_valido_y_queda_null(self):
        serializer = PeopleSerializer(data=self.datos)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        persona = serializer.save()
        self.assertIsNone(persona.lugar_votacion)
        self.assertIsNone(persona.mesa_votacion)

    def test_cadenas_vacias_se_normalizan_a_null(self):
        serializer = PeopleSerializer(data={
            **self.datos,
            'lugar_votacion': '   ',
            'mesa_votacion': '  ',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        persona = serializer.save()
        self.assertIsNone(persona.lugar_votacion)
        self.assertIsNone(persona.mesa_votacion)

    def test_texto_libre_sin_catalogo_es_valido(self):
        serializer = PeopleSerializer(data={
            **self.datos,
            'lugar_votacion': 'Puesto 44',
            'mesa_votacion': 'Mesa Z-9',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        persona = serializer.save()
        self.assertEqual(persona.lugar_votacion, 'Puesto 44')
        self.assertEqual(persona.mesa_votacion, 'Mesa Z-9')

    def test_mesa_sin_lugar_es_rechazada(self):
        serializer = PeopleSerializer(data={
            **self.datos,
            'mesa_votacion': 'Mesa 001',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('mesa_votacion', serializer.errors)

    def test_texto_se_recorta(self):
        serializer = PeopleSerializer(data={
            **self.datos,
            'lugar_votacion': '  Escuela Central  ',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        persona = serializer.save()
        self.assertEqual(persona.lugar_votacion, 'Escuela Central')

    def test_texto_demasiado_largo_es_rechazado(self):
        serializer = PeopleSerializer(data={
            **self.datos,
            'lugar_votacion': 'x' * 151,
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('lugar_votacion', serializer.errors)

    def test_actualizar_puede_dejar_sin_lugar(self):
        persona = People.objects.create(
            nombre='Ana', apellido='Ramos', telefono='04121234567', edad=40,
            urbanizacion='La Aurora', lugar_votacion='Escuela Central',
            mesa_votacion='Mesa 12',
        )

        serializer = PeopleSerializer(
            persona, data={'lugar_votacion': '', 'mesa_votacion': ''}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        persona.refresh_from_db()
        self.assertIsNone(persona.lugar_votacion)
        self.assertIsNone(persona.mesa_votacion)
