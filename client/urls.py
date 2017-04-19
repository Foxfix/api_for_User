from django.conf.urls import url 
from django.contrib import admin
from .views import client

urlpatterns = [
    url(r'^$', client, name='client'),
    
]
 