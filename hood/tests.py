from django.test import TestCase 
from .models import *
from django.contrib.auth.models import User

# Create your tests here.

class ProfileTestClass(TestCase):

    # Set up method
    def setUp(self):
        # Creating a new user and saving it
        self.brian= User(id=1, username='briankiiru', password='andela')
        # self.brian.save_user()
       

        self.hood= Hood(name = 'juja', location = 'juja')
        self.hood.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def tearDown(self):
        Profile.objects.all().delete()
        Hood.objects.all().delete()
