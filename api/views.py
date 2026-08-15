from rest_framework import viewsets
from person.models import Person
from user.models import User
from .serializers import PersonSerializer, UserSerializer
from rest_framework.authentication import *
from rest_framework.permissions import *

class PersonViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

