from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^personal', views.verify_personal, name='personal'),
    url(r'^business', views.verify_business, name='business'),
    url(r'^', views.test, name='test'),
]
