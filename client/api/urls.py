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


'''
curl -X POST -d "username=olga&password=223355aa" http://127.0.0.1:8000/api/token/
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im9sZ2EiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6IiIsImV4cCI6MTQ4MDYxNDYzNH0.-jWXU6VFrLtiokOX9QPISA1uZNGJv1tYAGPLhR__Gis
curl -X POST -d "username=olga2&password=223355aa" http://127.0.0.1:8000/api/token/
$ curl -H "Authorization: JWT " http://127.0.0.1:8000/api/16/
curl -X GET http://127.0.0.1:8000/api/1/


'''