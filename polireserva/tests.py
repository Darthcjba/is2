

from django.test import TestCase
from django.contrib.auth import SESSION_KEY
from polireserva.models import TdRecurso,Recurso
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_permission,has_role

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



class tdrTestCase(TestCase):
    def setUp(self):
        a1 = TdRecurso.objects.create(description="Aula")
        a2 = TdRecurso.objects.create(description="Proyector")
        Recurso.objects.create(name_r="A50", id_tdr=a1,description="objeto de prueba 1",date_c="2017-05-05",date_m="2017-05-05")
        Recurso.objects.create(name_r="A51", id_tdr=a1,description="objeto de prueba 2",date_c="2017-05-05",date_m="2017-05-05")
        Recurso.objects.create(name_r="epson", id_tdr=a2,description="objeto de prueba 3",date_c="2017-05-05",date_m="2017-05-05")

    def test_recurso_tdr(self):
        recurso1 = Recurso.objects.get(name_r="A51")
        tipo= TdRecurso.objects.get(id_tdr=recurso1.id_tdr.id_tdr)
        self.assertEqual(tipo.description, "Aula")


class userTestCase(TestCase):
    def setUp(self):
        user=User.objects.create(username="Matirivas1995",first_name="Mati",last_name="Rivas",email="matias.rt@hotmail.com",password="123456qwe")
        user1 = User.objects.create(username="Eliasmorag", first_name="Elias", last_name="Mora",email="emora@emora.com.py", password="altoqueroque")
        assign_role(user,'administrador')
        assign_role(user1,'usuario')


    def test_has_permission(self):
        usertest=User.objects.get(id=1)
        usertest2=User.objects.get(id=2)
        self.assertIs(has_permission(usertest,'can_access_admin'), True)
        self.assertIs(has_permission(usertest2, 'can_access_admin'), False)

    def test_has_role(self):
        usertest = User.objects.get(id=1)
        self.assertIs(has_role(usertest,'tecnico'),False)








