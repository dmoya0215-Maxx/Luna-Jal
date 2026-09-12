from rest_framework import viewsets
from people.models import People
from user.models import User
from .serializers import PeopleSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import BasePermission


def _esta_logueado(request):
    if request.session.get("logueado"):
        return True
    user = getattr(request.user, 'is_authenticated', False)
    return bool(user)


def _es_admin(request):
    sesion = request.session.get("logueado")
    if isinstance(sesion, dict) and str(sesion.get('rol', '')).strip().lower() == 'admin':
        return True
    user = request.user
    return bool(getattr(user, 'is_authenticated', False)) and bool(getattr(user, 'is_staff', False))


class IsLoggedIn(BasePermission):
    """Permite el acceso solo a usuarios autenticados del sistema o de Django."""
    def has_permission(self, request, view):
        return _esta_logueado(request)


class IsAdmin(BasePermission):
    """Permite el acceso solo a usuarios con cargo Admin (o staff de Django)."""
    def has_permission(self, request, view):
        return _es_admin(request)


class PeopleViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsLoggedIn]
    queryset = People.objects.all()
    serializer_class = PeopleSerializer


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer

