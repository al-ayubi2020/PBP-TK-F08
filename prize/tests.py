from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser, commonUser

from admin_page.models import Prize

from .views import *

class TestPrize(TestCase):

    def setUp(self):
        self.c = Client()
        Prize.objects.create(nama="test", poin=1, stok=0, desc="test")
        self.test1 =  User.objects.create(username="test1", password='12345')
        self.test2 =  User.objects.create(username="test2", password='12345')
        assign_role(self.test1, superUser)
        assign_role(self.test2, commonUser)
        self.c.force_login(self.test2)
        self.index = reverse('prize:index')
        self.index_redeem = reverse('prize:index_redeem')
        self.redeem = reverse('prize:redeem')
        self.prize = reverse('prize:prize')
    
    def test_urls_index(self):
        response = self.c.get(self.index)
        self.assertEquals(response.status_code , 200)

    def test_urls_index_redeem(self):
        response = self.c.get(self.index_redeem)
        self.assertEquals(response.status_code , 200)

    def test_urls_redeem(self):
        response = self.c.get(self.redeem)
        self.assertEquals(response.status_code , 200)

    def test_urls_redeem_prize(self):
        response = self.c.post('/prize/redeem/1/')
        self.assertEquals(response.status_code , 200)

    def test_urls_redeem_prize(self):
        response = self.c.post('/prize/redeem/useprize/1/')
        self.assertEquals(response.status_code , 200)

    def test_urls_prize(self):
        response = self.c.get(self.prize)
        self.assertEquals(response.status_code , 200)
    
    def test_view_index(self):
        self.assertEquals(resolve(self.index).func , index)

    def test_view_index_redeem(self):
        self.assertEquals(resolve(self.index_redeem).func , index_redeemed)

    def test_view_redeem(self):
        self.assertEquals(resolve(self.redeem).func , get_prize_redeem)

    def test_view_prize(self):
        self.assertEquals(resolve(self.prize).func , get_prize)

