from django.test import TestCase

# Create your tests here.


from django.test import Client
from choice.models import User
from django.contrib.auth import login
from .models import confirmation_code
from random import randint

def code_6():
    o=""
    for i in range(6):
        p=randint(1,9)
        o += str(p)
    return int(o)


class Pages(TestCase):
    def setUp(self):
        self.usr=Client()
        self.usrr=User.objects.create_user('essai', 'essai@essai.com', 'password')
    def test_login(self):
        response=self.usr.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
    def test_home(self):
        response=self.usr.post('/accounts/login/', {'Username':'essai',
                                                    'Password':'password'})
        self.assertRedirects(response, '/home/')
        response2 = self.usr.get('/home/')
        self.assertContains(response2, "Log out")
        self.assertNotContains(response2, "Log in")
    def test_home2(self):
        response=self.usr.post('/accounts/login/', {'Username':'essa',
                                                    'Password':'password'})
        self.assertTemplateUsed(response, 'authh/Login.html')
        self.assertContains(response, "Your password or")
    def test_logout(self):
        response=self.usr.post('/accounts/login/', {'Username':'essai',
        'Password':'password'})
        response2=self.usr.get('/accounts/logout/')
        self.assertEqual(response2.status_code, 302)

        self.assertEqual(response.status_code, 302)
   
    def test_password_forgotten_page_unlogged_in(self):
        response=self.usr.get('/accounts/reset_password/')
        self.assertEqual(response.status_code, 200)
    def test_password_forgotten_page_logged_in(self):
        a=self.usr.login(username="essai", password="password")
        response=self.usr.get('/accounts/reset_password/')
        self.assertEqual(response.status_code, 302)

class objets(TestCase):
    def setUp(self):
        self.usr=User.objects.create_user('essai', 'essai@essai.com', 'essayons')
        self.client=Client()
    def test_change_password(self):
        a=self.client.post('/accounts/reset_password/', {'Username':'essai'})
        b=self.client.post('/accounts/reset_password/', {'Username':'essai'})
        t=len(self.usr.confirmation_code_set.all())
        r=self.usr.confirmation_code_set.get(pk=1)
        cc=r.num
        u=r.qualified
        self.assertEqual(t, 1)
        self.assertEqual(len(str(cc)), 6)
        self.assertEqual(type(cc), int)
        self.assertEqual(u, True)
    def test_conf_code(self):
        a=self.client.login(username="essai", password="essayons")
        b=self.client.get('/accounts/reset_password_confirm/essai/')
        self.assertEqual(b.status_code, 302)
    def test_confirm_code_true(self):
        a=self.client.post('/accounts/reset_password/', {'Username':'essai'})
        code=self.usr.confirmation_code_set.get(pk=1)
        b=self.client.post('/accounts/reset_password_confirm/essai/', {'code':code.num})
        code2=self.usr.confirmation_code_set.get(pk=1)
        self.assertEqual(code2.qualified, False)
    def test_confirm_code_false(self):
        a=self.client.post('/accounts/reset_password/', {'Username':'essai'})
        code=self.usr.confirmation_code_set.get(pk=1)
        u=code
        while u==code:
            u=code_6()
        b=self.client.post('/accounts/reset_password_confirm/essai/', {'code':u})
        self.assertContains(b, "Ce n est pas le bon code. Veuillez reessayer ou reinitialiser votre formulaire")
    def test_confirm_code_success(self):
        a=self.client.post('/accounts/reset_password/', {'Username':'essai'})
        code=self.usr.confirmation_code_set.get(ref=1)
        b=self.client.post('/accounts/reset_password_confirm/essai/', {'code':code.num})
        uu=self.usr.confirmation_code_set.get(ref=1)
        self.assertEqual(uu.confirm, True)
        c=self.client.get('/accounts/reset_password/success/essai/')
        self.assertEqual(c.status_code, 200)
    def test_access_success_page(self):
        a=self.client.post('/accounts/login/', {"Username":"essai", "Password":"essayons"})
        b=self.client.get('/accounts/change_password_success/')
        c=self.client.post('/accounts/change_password/', {'Old password':"essayons", "New password":"Avionner1245", "New password confirmation":"Avionner1245"}, follow=True,)
        self.assertEqual(c.status_code, 200)
        self.assertContains(c, "!")
        self.assertEqual(b.status_code, 302)
        d=self.client.get("/accounts/logout/")
        self.assertEqual(d.status_code, 302)
