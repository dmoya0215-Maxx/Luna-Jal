from django.core.exceptions import ValidationError
from django.db import models


URBANIZACIONES = [
    ("Luna del Mar", "Luna del Mar"),
    ("Luna del Campo", "Luna del Campo"),
    ("Luna del Bosque", "Luna del Bosque"),
    ("Luna del Valle", "Luna del Valle"),
    ("Luna del Cerro", "Luna del Cerro"),
    ("Luna del Viento", "Luna del Viento"),
    ("Bosques de la Macarena", "Bosques de la Macarena"),
    ("Altos Macarena", "Altos Macarena"),
    ("Atardeceres", "Atardeceres"),
    ("Corregimiento de San Cristóbal", "Corregimiento de San Cristóbal"),
    ("Mirador de la Huerta", "Mirador de la Huerta"),
    ("Cantares I", "Cantares I"),
    ("Cantares II", "Cantares II"),
    ("Cantares III", "Cantares III"),
    ("Cantares IV", "Cantares IV"),
    ("Cantares V", "Cantares V"),
    ("La Aurora", "La Aurora"),
    ("Aurora de la Libertad", "Aurora de la Libertad"),
    ("Renaceres", "Renaceres"),
    ("Veletas", "Veletas"),
    ("Nazareth", "Nazareth"),
    ("Montaña", "Montaña"),
    ("Las Flores", "Las Flores"),
    ("Pedregal Alto", "Pedregal Alto"),
    ("Chagualón", "Chagualón"),
    ("La Cascada", "La Cascada"),
    ("Mirador de la Cascada", "Mirador de la Cascada"),
    ("Tirol 1", "Tirol 1"),
    ("Tirol 2", "Tirol 2"),
    ("Tirol 3", "Tirol 3"),
    ("Villa Suramericana", "Villa Suramericana"),
    ("Mirador del Valle", "Mirador del Valle"),
    ("Ventro 1", "Ventro 1"),
    ("Puerta del Sol", "Puerta del Sol"),
    ("Málaga", "Málaga"),
]

VEREDA_PREFIX = "S.C "

VEREDAS = [
    "Boquerón",
    "San José de la Montaña",
    "La Ilusión",
    "El Yolombo",
    "El Carmelo",
    "El Picacho",
    "Pajarito",
    "Pedregal Alto",
    "Pedregal Bajo",
    "Travesías",
    "El Llano",
    "Naranjal",
    "La Cuchilla",
    "El Uvito",
    "Las Playas",
    "El Patio",
    "La Palma",
    "La Loma",
]

for _vereda in VEREDAS:
    URBANIZACIONES.append((f"{VEREDA_PREFIX}{_vereda}", f"{VEREDA_PREFIX}{_vereda}"))


class People(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=150, blank=True, null=True)
    edad = models.PositiveIntegerField()
    urbanizacion = models.CharField(max_length=100)
    lugar_votacion = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Lugar de votación',
        help_text='Opcional. Si se deja vacío se guarda sin valor (NULL).',
    )
    mesa_votacion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Mesa de votación',
        help_text='Opcional. Requiere un lugar de votación.',
    )
    referido_por = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referidos"
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if (
            self.referido_por is not None
            and self.pk is not None
            and self.referido_por_id == self.pk
        ):
            raise ValidationError({
                'referido_por': 'Una persona no puede referirse a sí misma.'
            })

        if not self.lugar_votacion and self.mesa_votacion:
            raise ValidationError({
                'mesa_votacion': 'Debe indicar un lugar de votación para asignar una mesa.'
            })

    def __str__(self):
        return f"{self.nombre} {self.apellido}"