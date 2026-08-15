from rest_framework import viewsets
from people.models import People
from user.models import User
from .serializers import PeopleSerializer, UserSerializer
from rest_framework.authentication import *
from rest_framework.permissions import *

class PeopleViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = People.objects.all()
    serializer_class = PeopleSerializer


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

