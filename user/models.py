from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    nombre = models.CharField(max_length=254, unique=True)
    contraseña = models.CharField(max_length=255)  # Aumentado para almacenar hash
    CARGO = (
        ("Admin", "ADMIN"),
        ("Invitado", "INVITADO")
    )
    cargo = models.CharField(max_length=254, choices=CARGO, default="Invitado")
    fecha_creacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    def set_password(self, raw_password):
        """Hashea y almacena la contraseña"""
        self.contraseña = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifica la contraseña contra el hash almacenado"""
        return check_password(raw_password, self.contraseña)
