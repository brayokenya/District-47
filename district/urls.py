from django.conf.urls import url
from . import views
from django.conf.urls import include
from django.urls import path

urlpatterns=[

     url('^$',views.index,name='dist'),


]