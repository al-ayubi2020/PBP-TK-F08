from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser, commonUser

class TestUrls(TestCase):

    def setUp(self):
        self.c = Client()
        self.test1 =  User.objects.create(username="test1", password='12345')
        self.test2 =  User.objects.create(username="test2", password='12345')
        assign_role(self.test1, superUser)
        assign_role(self.test2, commonUser)
        self.c.force_login(self.test2)
        self.index = reverse('prize:index')
        self.index_redeem = reverse('prize:index_redeem')
        self.redeem = reverse('prize:redeem')
    
    def test_urls_index(self):
        response = self.c.get(self.index)
        self.assertEquals(response.status_code , 200)

    def test_urls_index_redeem(self):
        response = self.c.get(self.index_redeem)
        self.assertEquals(response.status_code , 200)

    def test_urls_redeem(self):
        response = self.c.get(self.redeem)
        self.assertEquals(response.status_code , 200)