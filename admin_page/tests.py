from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser, commonUser
from .models import UserData, Prize
from deposit.models import Deposit


# Create your tests here.

class TestUrls(TestCase):

    def setUp(self):
        self.c = Client()
        self.test1 =  User.objects.create(username="test1", password='12345')
        self.test2 =  User.objects.create(username="test2", password='12345')
        UserData.objects.create(user=self.test2)
        assign_role(self.test1, superUser)
        assign_role(self.test2, commonUser)
        Deposit.objects.create(user=self.test2, username=self.test2.get_username(), jenisSampah="Plastik", beratSampah=1, isApprove='PENDING', poin=0, totalHarga=0)
        Deposit.objects.create(user=self.test2, username=self.test2.get_username(), jenisSampah="Plastik", beratSampah=1, isApprove='PENDING', poin=0, totalHarga=0)
        self.c.force_login(self.test1)
        self.index = reverse('admin_page:index')
        self.deposit = reverse('admin_page:deposit')
        self.get_deposit = reverse('admin_page:get_deposit')
        self.get_deposit_count = reverse('admin_page:get_deposit_count')
        self.add_deposit = reverse('admin_page:add_deposit') # kerjain nanti
        self.del_deposit = reverse('admin_page:del_deposit2')
        self.acc_deposit = reverse('admin_page:acc_deposit')
        self.prize = reverse('admin_page:prize')
        self.add_prize = reverse('admin_page:add_prize') # kerjain nanti
        self.get_prize = reverse('admin_page:get_prize')
        # self.del_prize = reverse('/prize/del/1')
        self.login_user = reverse('admin_page:login_user')
        self.register = reverse('admin_page:register')
        self.logout_user = reverse('admin_page:logout_user')

    def test_urls_index(self):
        response = self.c.get(self.index)
        self.assertEquals(response.status_code , 200)
    
    def test_urls_deposit(self):
        response = self.c.get(self.deposit)
        self.assertEquals(response.status_code , 200)
    
    def test_urls_get_deposit(self):
        response = self.c.get(self.get_deposit)
        self.assertEquals(response.status_code , 200)
    
    def test_urls_get_deposit_count(self):
        response = self.c.get(self.get_deposit_count)
        self.assertEquals(response.status_code , 200)
    
    def test_urls_add_deposit(self):
        test3 = User.objects.get(username=self.test2.get_username())
        response = self.c.post(self.add_deposit, {'username' : test3.get_username(), 'jenisSampah' : 'PLASTIK', 'beratSampah' : 0})
        self.assertEquals(response.status_code , 200)
    
    def test_urls_del_deposit(self):
        response = self.c.post(self.del_deposit, {'id' : 1})
        self.assertEquals(response.status_code , 200)
    
    def test_urls_acc_deposit(self):
        response = self.c.post(self.acc_deposit, {'id' : 2})
        self.assertEquals(response.status_code , 200)

    def test_urls_prize(self):
        response = self.c.get(self.prize)
        self.assertEquals(response.status_code , 200)

    def test_urls_get_prize(self):
        response = self.c.get(self.get_prize)
        self.assertEquals(response.status_code , 200)

    def test_urls_login_user(self):
        response = self.c.get(self.login_user)
        self.assertEquals(response.status_code , 200)

    def test_urls_register(self):
        response = self.c.get(self.register)
        self.assertEquals(response.status_code , 200)

    