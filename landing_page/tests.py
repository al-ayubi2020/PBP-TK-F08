from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser, commonUser

from admin_page.models import Prize

from .views import *

class TestLanding(TestCase):

    def setUp(self):
        self.c = Client()
        Prize.objects.create(nama="test", poin=1, stok=0, desc="test")
        self.test1 =  User.objects.create(username="test1", password='12345')
        self.test2 =  User.objects.create(username="test2", password='12345')
        assign_role(self.test1, superUser)
        assign_role(self.test2, commonUser)
        self.c.force_login(self.test2)
        self.index = reverse('landing_page:index')
        self.add_testimoni = reverse('landing_page:add_testimoni')
        self.get_testimoni = reverse('landing_page:get_testimoni')
        self.register = reverse('landing_page:register')
        self.login = reverse('landing_page:login')
        self.logout = reverse('landing_page:logout')
    
    def test_urls_index(self):
        response = self.c.get(self.index)
        self.assertEquals(response.status_code , 200)

    def test_post_add_testimoni(self):
        response = self.c.post(self.add_testimoni)
        self.assertEquals(response.status_code , 200)

    def test_urls_get_testimoni(self):
        response = self.c.get(self.get_testimoni)
        self.assertEquals(response.status_code , 200)

    def test_urls_register(self):
        response = self.c.get(self.register)
        self.assertEquals(response.status_code , 200)

    def test_urls_login(self):
        response = self.c.get(self.login)
        self.assertEquals(response.status_code , 200)

    def test_post_login(self):
        response = self.c.post(self.login ,{'username': 'test2','password':'12345'})
        self.assertEquals(response.status_code , 200)

    def test_post_register(self):
        response = self.c.post(self.register,{'username': 'test2','password':'12345'})
        self.assertEquals(response.status_code , 200)
    
    def test_view_index(self):
        self.assertEquals(resolve(self.index).func , index)

    def test_view_add_testimoni(self):
        self.assertEquals(resolve(self.add_testimoni).func , add_testimoni)

    def test_view_get_testimoni(self):
        self.assertEquals(resolve(self.get_testimoni).func , get_testimoni)

    def test_view_register(self):
        self.assertEquals(resolve(self.register).func , register)

    def test_view_login(self):
        self.assertEquals(resolve(self.login).func , login_user)
    
    def test_view_logout(self):
        self.assertEquals(resolve(self.logout).func , logout_user)

    def test_template_index(self):
        response = self.c.get(self.index)
        self.assertEquals(response.status_code , 200)
        self.assertTemplateUsed(response, 'index_landing.html')