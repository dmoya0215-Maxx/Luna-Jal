from rest_framework import serializers
from django.utils import timezone
from people.models import People
from user.models import User

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'

    def validate_lugar_votacion(self, value):
        """Texto libre opcional: vacío o solo espacios se guarda como NULL."""
        lugar = (value or '').strip()
        if len(lugar) > 150:
            raise serializers.ValidationError(
                'El lugar de votación no puede superar los 150 caracteres.'
            )
        return lugar or None

    def validate_mesa_votacion(self, value):
        """Texto libre opcional, con la misma regla que el formulario web."""
        mesa = (value or '').strip()
        if not mesa:
            return None
        if len(mesa) > 100:
            raise serializers.ValidationError(
                'La mesa de votación no puede superar los 100 caracteres.'
            )
        return mesa

    def validate(self, attrs):
        """La API no pasa por PersonForm, así que se replica la regla de integridad."""
        instancia = self.instance

        lugar = attrs.get(
            'lugar_votacion',
            instancia.lugar_votacion if instancia else None,
        )
        mesa = attrs.get(
            'mesa_votacion',
            instancia.mesa_votacion if instancia else None,
        )

        if not lugar and mesa:
            raise serializers.ValidationError({
                'mesa_votacion': 'Indique primero el lugar de votación para asignar una mesa.'
            })

        return attrs


class UserSerializer(serializers.ModelSerializer):
    contraseña = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        min_length=6
    )

    class Meta:
        model = User
        fields = ('id', 'nombre', 'contraseña', 'cargo', 'fecha_creacion')

    def create(self, validated_data):
        contraseña = validated_data.pop('contraseña', None)
        user = User(**validated_data)
        if not user.fecha_creacion:
            user.fecha_creacion = timezone.now()
        if contraseña:
            user.set_password(contraseña)
        user.save()
        return user

    def update(self, instance, validated_data):
        contraseña = validated_data.pop('contraseña', None)
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        if contraseña:
            instance.set_password(contraseña)
        instance.save()
        return instance