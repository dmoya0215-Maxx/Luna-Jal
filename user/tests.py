from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from .models import User
from .views import DeleteUser


class DeleteUserAccessTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = User.objects.create(
            nombre='admin_user',
            contraseña='hash',
            cargo='Admin'
        )
        self.normal_user = User.objects.create(
            nombre='normal_user',
            contraseña='hash',
            cargo='Invitado'
        )

    def _build_request(self, path, method='POST', session_user=None):
        request = getattr(self.factory, method.lower())(path)
        SessionMiddleware(lambda req: None).process_request(request)
        if session_user is not None:
            request.session['logueado'] = session_user
        request.session.save()
        setattr(request, '_messages', FallbackStorage(request))
        return request

    def test_admin_cannot_delete_another_admin(self):
        request = self._build_request(
            f'/user/delete/{self.admin_user.id}/',
            method='POST',
            session_user={'id': self.admin_user.id, 'nombre': self.admin_user.nombre, 'rol': 'Admin'}
        )

        with self.assertRaises(PermissionDenied):
            DeleteUser(request, self.admin_user.id)

        self.assertTrue(User.objects.filter(id=self.admin_user.id).exists())

    def test_admin_can_delete_a_non_admin_user(self):
        request = self._build_request(
            f'/user/delete/{self.normal_user.id}/',
            method='POST',
            session_user={'id': self.admin_user.id, 'nombre': self.admin_user.nombre, 'rol': 'Admin'}
        )

        response = DeleteUser(request, self.normal_user.id)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.normal_user.id).exists())
