from django.conf.urls import url, include
from django.contrib import admin
from client.views import (login_view, register_view, logout_view)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^api/', include("client.api.urls", namespace='api')),
    url(r'^', include("client.urls")),
]
