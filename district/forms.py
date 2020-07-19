from .models import *
from django import forms
from django.contrib.auth.models import User


# Register a new User Form
class UserForm(forms.ModelForm):
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={"class":"form-control mb-3",
                                                               "placeholder":"First Name"}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={"class":"form-control mb-3",
                                                               "placeholder":"Last Name"}))
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={"class":"form-control mb-3",
                                                               "placeholder":"Username"}))
    email = forms.CharField(label=False, widget=forms.TextInput(attrs={"class":"form-control mb-3",
                                                               "placeholder":"Email"}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={"class":"form-control mb-3",
                                                               "placeholder":"Password"}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password",)


#User Profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("profile_pic", "phone_number", "bio",)

class NeighbourHoodForm(forms.ModelForm):
    class Meta:
        model = NeighbourHood
        exclude = ('admin',)


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('user', 'neighbourhood')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'hood')