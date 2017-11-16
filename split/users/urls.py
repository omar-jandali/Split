from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^', views.test, name='test'),
]
