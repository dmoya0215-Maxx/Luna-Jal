from rest_framework import serializers
from django.utils import timezone
from people.models import People
from user.models import User

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'


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