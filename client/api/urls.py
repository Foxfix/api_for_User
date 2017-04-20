from django.conf.urls import url, include
# from rest_framework import routers
from .views import (UserListView, 
                    UserDetailView,
                    UserCreateAPIView,
                    UserLoginAPIView)
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^token/$',  obtain_jwt_token),
    url(r'^(?P<pk>\d+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^', UserListView.as_view(), name='list'), 

]


