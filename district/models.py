from django.db import models
import datetime as dt
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = CloudinaryField('profile_pic')
    phone_number = models.CharField(max_length = 10,blank =True)
    bio = models.TextField(blank=True)
    email = models.CharField(max_length=250)
    estate = models.ForeignKey('Neighbourhood', on_delete=models.CASCADE, blank=True, null=True,related_name='people')
   
    
    def __str__(self):
        return f'{self.user.username} profile'

    def save_userprofile(self):
        self.save()  

    def delete_userprofile(self):
        self.delete()

    def update_bio(self, bio):
        self.bio = bio
        self.save()

class NeighbourHood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    admin = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name='hood')
    logo = CloudinaryField('Hood-logo')
    description = models.TextField()
    health_tell = models.IntegerField(null=True, blank=True)
    police_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} hood'

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls, neighborhood_id):
        return cls.objects.filter(id=neighborhood_id)


class Business(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='business')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f'{self.name} Business'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()


class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_owner')
    hood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='hood_post')