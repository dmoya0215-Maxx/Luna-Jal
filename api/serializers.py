from rest_framework import serializers
from person.models import Person
from user.models import User

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['contraseña']