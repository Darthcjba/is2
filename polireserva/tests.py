from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Usuario
from .models import TdRecurso
from django.contrib.auth import SESSION_KEY
from django.utils import timezone


class LoginTest(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'test')

    def test_login_existing_user(self):
        u = User.objects.get(username='test')
        self.assertIsNotNone(u)
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)

    def test_login_non_existing_user(self):
        self.assertEqual(User.objects.filter(username='nobody').count(), 0)
        c = self.client
        login = c.login(username='nobody', password='nobody')
        self.assertFalse(login)

    def test_login_wrong_password(self):
        u = User.objects.get(username='test')
        self.assertIsNotNone(u)
        c = self.client
        pw = 'wrong'
        self.assertFalse(u.check_password(pw))
        login = c.login(username='test', password=pw)
        self.assertFalse(login)

    def test_logout_after_login(self):
        u = User.objects.get(username='test')
        self.assertIsNotNone(u)
        c = self.client
        login = c.login(username='test', password='test')
        self.assertTrue(login)
        c.logout()
        self.assertTrue(SESSION_KEY not in self.client.session)


class test_TDR(TestCase):

    def setUp(self):
        TdRecurso.objects.create('123', 'Descripcion')

    def test_modificar(self):
        t = TdRecurso.objects.get(id_tdr='123')
