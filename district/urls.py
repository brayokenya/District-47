from django.conf.urls import url
from . import views
from django.conf.urls import include
from django.urls import path

urlpatterns=[

    url('^$',views.index,name='dist'),
    url(r"^profile/(\d+)", views.profile, name="profile"),
    url(r'^myprofile/$',views.my_profile,name = 'my-profile'),
    url(r'^register/$',views.register,name='register'),
    url(r'^createprofile/$',views.create_profile,name = 'create-profile'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^accounts/login/$',views.user_login,name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),

]