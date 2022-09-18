from django.test import TestCase

# Create your tests here.

from django.test import Client
from choice.models import User, dish
from .forms import choice_form

class test_pages(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("Essai", "essai@try.com", "again@123" )
        o1=dish.objects.create(choices="dish1", ref=1)
        o2=dish.objects.create(choices="dish2", ref=2)
        
        
    def test_order(self):
        a = self.client.post("/accounts/login/", {"Username":"Essai", "Password":"again@123"})
        b = self.client.get("/choice/")
        self.assertEqual(b.status_code, 200)
       
        
        
        
        
