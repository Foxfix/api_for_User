from django.conf.urls import url, include
from django.contrib import admin
from client.views import (login_view, register_view, logout_view)
# from rest_framework_jwt.views import verify_jwt_token


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    # url(r'^api/auth/token/', verify_jwt_token),
    url(r'^api/', include("client.api.urls", namespace='api')),
    url(r'^', include("client.urls")),
]


'''

curl -X POST -d "username=user&password=111111" http://127.0.0.1:8000/api/auth/token/
curl -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0OTI1NjcxMDYsImVtYWlsIjoiMUBtYWlsLnJ1IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJvbGdhIn0.Iw29z_v9t-pzXySyn3cTzVyMzSx04hks74KXynnR_yo" http://127.0.0.1:8000/api/

'''