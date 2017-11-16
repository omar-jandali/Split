from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^personal', views.verify_personal, name='personal'),
    url(r'^business', views.verify_business, name='business'),
    url(r'^test', views.test, name='test'),
    url(r'^', views.home, name='home'),
]
