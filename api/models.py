from django.db import models


class Servicio(models.Model):
    nombre = models.CharField(max_length=254)
    costo = models.IntegerField()
    descripcion = models.TextField(
        null=True,
        blank=True
    )

    ESTADOS = (
        ("Activo", "ACTIVO"),
        ("Inactivo", "INACTIVO"),
    )

    estado = models.CharField(
        max_length=8,
        choices=ESTADOS,
        default="Activo"
    )

    def __str__(self):
        return f"{self.nombre} ({self.costo})"